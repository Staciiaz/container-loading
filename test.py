import math


def test():
    data = [3, 5, 10, 8, 4]
    sum_score = 0
    n = sum(data)
    for i, d in enumerate(data):
        sum_score += (i + 1) * d
    mean_score = sum_score / n
    sum_std_dev = 0
    for i, d in enumerate(data):
        sum_std_dev += math.pow((i + 1) - mean_score, 2) * d
    std_dev = math.sqrt(sum_std_dev / (n - 1))
    print('Mean: {0:.4f}'.format(mean_score))
    print('Std. Dev: {0:.4f}'.format(std_dev))


if __name__ == '__main__':
    test()
