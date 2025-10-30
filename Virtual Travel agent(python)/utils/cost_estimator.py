import logging

def calculate_total_cost(itinerary, travelers=1):
    """
    Calculate total cost breakdown for the itinerary
    """
    try:
        # Base costs (these would come from actual API data in production)
        flight_cost = 450  # Base flight cost per person
        hotel_cost_per_night = 120  # Base hotel cost per night
        activity_cost_per_day = 50  # Base activity cost per day

        # Calculate duration
        days = len(itinerary.get('days', []))
        nights = max(0, days - 1) if days > 0 else 0

        # Calculate costs
        flights = flight_cost * travelers
        hotels = hotel_cost_per_night * nights * travelers
        activities = activity_cost_per_day * days * travelers
        misc = (flights + hotels + activities) * 0.1  # 10% for miscellaneous

        total = flights + hotels + activities + misc

        return {
            'flights': round(flights, 2),
            'hotels': round(hotels, 2),
            'activities': round(activities, 2),
            'misc': round(misc, 2),
            'total': round(total, 2),
            'per_person': round(total / travelers, 2) if travelers > 0 else 0
        }

    except Exception as e:
        logging.error(f"Error calculating costs: {str(e)}")
        return {
            'flights': 0,
            'hotels': 0,
            'activities': 0,
            'misc': 0,
            'total': 0,
            'per_person': 0
        }

def get_cost_variants(itinerary, travelers=1, budget=None):
    """
    Provide cost variants (economy, balanced, premium)
    """
    base_costs = calculate_total_cost(itinerary, travelers)

    variants = {
        'economy': {
            'multiplier': 0.8,
            'description': 'Budget-friendly options'
        },
        'balanced': {
            'multiplier': 1.0,
            'description': 'Balanced comfort and cost'
        },
        'premium': {
            'multiplier': 1.3,
            'description': 'Luxury experience'
        }
    }

    for variant, config in variants.items():
        variants[variant]['total'] = round(base_costs['total'] * config['multiplier'], 2)
        variants[variant]['per_person'] = round(variants[variant]['total'] / travelers, 2)

    return variants

def validate_budget(total_cost, budget, travelers=1):
    """
    Check if total cost fits within budget
    """
    return total_cost <= budget
