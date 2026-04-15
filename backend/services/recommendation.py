def get_recommendation(crop):

    if crop == "rice":
        return "Irrigate every 5 days"

    elif crop == "wheat":
        return "Irrigate every 7 days"

    else:
        return "Follow standard irrigation practices"