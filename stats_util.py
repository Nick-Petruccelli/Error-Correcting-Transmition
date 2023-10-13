class StatsUtil:

    @staticmethod
    def choose(n, m):
        return StatsUtil.factorial(n)/(StatsUtil.factorial(m)*StatsUtil.factorial(n-m))

    @staticmethod
    def factorial(n):
        product = 1
        for x in range(n):
            product *= (x+1)
        return product
    
    @staticmethod
    def binom_dist(
        num_success: int,
        trials: int,
        prob_of_success: float
    )->float:
        """
        calculates binomeal distribution of random variable X or less
        :param num_success: number of success
        :param trials: number of trials
        :param prob_of_success: probability of success
        """
        probability_sum = 0
        for i in range(0,num_success+1):
            probability_sum += StatsUtil.choose(trials,i)*(prob_of_success**i)*((1-prob_of_success)**(trials-i))
        return probability_sum
    
if __name__ == "__main__":
    print(StatsUtil.binom_dist(2,3,.9999))

    print(StatsUtil.choose(1,1))

    prob = StatsUtil.binom_dist(1//2, 1, .0001)
        
    prob = 1-(prob)**328648
    print(prob)