import pandas as pd
import os
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

class RSVPManager:
    def __init__(self):
        self.data_dir = 'data'
        self.rsvp_file = os.path.join(self.data_dir, 'rsvps.csv')
        self._ensure_data_dir()
        self._setup_google_sheets()
        self._setup_email()

    def _ensure_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _setup_google_sheets(self):
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            self.gc = gspread.authorize(creds)
            self.sheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
            self.sheet = self.gc.open_by_key(self.sheet_id).sheet1
        except Exception as e:
            logger.warning(f"Google Sheets setup failed: {e}. Using CSV only.")
            self.sheet = None

    def _setup_email(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')

    def add_rsvp(self, event_id, rsvp_data):
        rsvp_data['event_id'] = event_id
        rsvp_data['status'] = rsvp_data.get('status', 'attending')

        # Add to CSV
        rsvps_df = pd.read_csv(self.rsvp_file) if os.path.exists(self.rsvp_file) else pd.DataFrame()
        rsvps_df = pd.concat([rsvps_df, pd.DataFrame([rsvp_data])], ignore_index=True)
        rsvps_df.to_csv(self.rsvp_file, index=False)

        # Sync to Google Sheets
        if self.sheet:
            try:
                self.sheet.append_row(list(rsvp_data.values()))
            except Exception as e:
                logger.error(f"Failed to sync to Google Sheets: {e}")

        # Send confirmation email
        self._send_confirmation_email(rsvp_data)

        logger.info(f"RSVP added for event {event_id}: {rsvp_data['name']}")

    def get_rsvps(self, event_id):
        if not os.path.exists(self.rsvp_file):
            return []
        rsvps_df = pd.read_csv(self.rsvp_file)
        return rsvps_df[rsvps_df['event_id'] == int(event_id)].to_dict('records')

    def update_rsvp(self, event_id, attendee_id, updates):
        rsvps_df = pd.read_csv(self.rsvp_file)
        mask = (rsvps_df['event_id'] == int(event_id)) & (rsvps_df['id'] == int(attendee_id))
        for key, value in updates.items():
            rsvps_df.loc[mask, key] = value
        rsvps_df.to_csv(self.rsvp_file, index=False)

        # Update Google Sheets (simplified - would need row matching)
        if self.sheet:
            try:
                # Find and update row
                pass  # Implementation would require fetching all rows and updating
            except Exception as e:
                logger.error(f"Failed to update Google Sheets: {e}")

        logger.info(f"RSVP updated for event {event_id}, attendee {attendee_id}")

    def delete_rsvp(self, event_id, attendee_id):
        rsvps_df = pd.read_csv(self.rsvp_file)
        mask = (rsvps_df['event_id'] == int(event_id)) & (rsvps_df['id'] == int(attendee_id))
        rsvps_df = rsvps_df[~mask]
        rsvps_df.to_csv(self.rsvp_file, index=False)

        # Delete from Google Sheets (simplified)
        if self.sheet:
            try:
                pass  # Implementation would require row deletion
            except Exception as e:
                logger.error(f"Failed to delete from Google Sheets: {e}")

        logger.info(f"RSVP deleted for event {event_id}, attendee {attendee_id}")

    def _send_confirmation_email(self, rsvp_data):
        if not all([self.smtp_server, self.smtp_username, self.smtp_password]):
            logger.warning("Email not configured. Skipping confirmation.")
            return

        msg = MIMEText(f"Thank you for your RSVP, {rsvp_data['name']}! Your status is {rsvp_data['status']}.")
        msg['Subject'] = 'RSVP Confirmation'
        msg['From'] = self.smtp_username
        msg['To'] = rsvp_data['email']

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.smtp_username, rsvp_data['email'], msg.as_string())
            server.quit()
            logger.info(f"Confirmation email sent to {rsvp_data['email']}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
