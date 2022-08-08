from cv2 import exp


def calculate_PAC(num_of_samples, lowerboud, upperbound, epsilon, delta):
    prob = exp(-((2 * num_of_samples * epsilon ^ 2)/((upperbound - lowerboud)^ 2)))

    return prob

