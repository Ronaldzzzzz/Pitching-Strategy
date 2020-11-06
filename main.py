from experta import *
import json

class PitchingStrategy(KnowledgeEngine):
    @DefFacts()
    def start(self):
        print("\nHello! This is an expert system that to help you to select the pitching strategy based on the situation!")
        print("I will ask you a few questions about this plate appearance. And then I will also tell you where/how you should pitch.\n\n")
        yield Fact(action = "pitching")

    # ---------------- Facts ---------------- 

    @Rule(Fact(action = "pitching"), NOT(Fact(runner_1 = W())))
    def runner_at_1(self):
        self.runner_1 = input("Is there a runner on 1B (yes/no)? \n")
        self.declare(Fact(runner_1 = self.runner_1.lower()))
    
    @Rule(Fact(action = "pitching"), NOT(Fact(runner_2 = W())))
    def runner_at_2(self):
        self.runner_2 = input("Is there a runner on 2B (yes/no)? \n")
        self.declare(Fact(runner_2 = self.runner_2.lower()))
    
    @Rule(Fact(action = "pitching"), NOT(Fact(runner_3 = W())))
    def runner_at_3(self):
        self.runner_3 = input("Is there a runner on 3B (yes/no)? \n")
        self.declare(Fact(runner_3 = self.runner_3.lower()))

    @Rule(Fact(action = "pitching"), NOT(Fact(balls = W())))
    def num_of_balls(self):
        self.balls = input("How many balls are there (0-3)? \n")
        self.declare(Fact(balls = self.balls))
    
    @Rule(Fact(action = "pitching"), NOT(Fact(strikes = W())))
    def num_of_strikes(self):
        self.strikes = input("How many strikes are there (0-2)? \n")
        self.declare(Fact(strikes = self.strikes))

    @Rule(Fact(action = "pitching"), NOT(Fact(our_scored = W())), salience = 98)
    def num_of_our_scored(self):
        self.our_scored = int(input("How many runs has YOUR TEAM scored ? \n"))
        self.declare(Fact(our_scored = self.our_scored))
    
    @Rule(Fact(action = "pitching"), NOT(Fact(rival_scored = W())), salience = 98)
    def num_of_rival_scored(self):
        self.rival_scored = int(input("How many runs has the RIVAL TEAM scored ? \n"))
        self.declare(Fact(rival_scored = self.rival_scored))

    @Rule(Fact(action = "pitching"), NOT(Fact(batter_spot = W())))
    def batter_spot(self):
        self.batter_spot = input("What spot is the batter in the lineup (1-9)? \n")
        self.declare(Fact(batter_spot = self.batter_spot))

    @Rule(Fact(action = "pitching"), NOT(Fact(batter_chased = W())))
    def has_batter_chased(self):
        self.batter_chased = input("Has the batter chased one of the last pitches outside the strike zone (yes/no)? \n")
        self.declare(Fact(batter_chased = self.batter_chased.lower()))

    @Rule(Fact(action = "pitching"), NOT(Fact(pitching_accuracy = W())))
    def pitching_accuracy(self):
        self.pitching_accuracy = int(input("On a scale of 1-10, 10 being very accurate, how accurately is the pitcher throwing (1-10)? \n"))
        self.declare(Fact(pitching_accuracy = self.pitching_accuracy))

    @Rule(Fact(action = "pitching"), NOT(Fact(outs = W())))
    def num_of_outs(self):
        self.outs = input("How many outs are there in this inning(0-2)? \n")
        self.declare(Fact(outs = self.outs))
    
    @Rule(Fact(action = "pitching"), NOT(Fact(pitcher_position = W())))
    def p_position(self):
        self.pitcher_position = input("What is the position of the pitcher (SP, RP, CP)? \n")
        self.declare(Fact(pitcher_position = self.pitcher_position))

    @Rule(Fact(action = "pitching"), NOT(Fact(late_innings = W())))
    def innings_now(self):
        self.innings = int(input("What inning is it (0-9)? \n"))
        if self.innings < 7:
            self.declare(Fact(late_innings = "no"))
        else:
            self.declare(Fact(late_innings = "yes"))
    
    # ---------------- Rules ---------------- 

    @Rule(Fact(action = "pitching"), OR(Fact(runner_2 = "yes"), Fact(runner_3 = "yes")))
    def scoring_position_1(self):
        self.declare(Fact(scoring_position = "yes"))
    
    @Rule(Fact(action = "pitching"), AND(Fact(runner_2 = "no"), Fact(runner_3 = "no")))
    def scoring_position_2(self):
        self.declare(Fact(scoring_position = "no"))

    @Rule(Fact(action = "pitching"), 
    NOT(Fact(power = W())), 
    NOT(Fact(pitcher_position = "CP"),
    Fact(pitcher_position = MATCH.pitcher_position), 
    TEST(lambda pitcher_position: pitcher_position == "RP")))
    def innings_thrown(self):
        self.thrown = input("How many innings has the pitcher thrown today (0-8)? \n")
        self.thrown = int(self.thrown)

        if self.thrown <= 1:
            self.declare(Fact(power = "good"))
        elif self.thrown <= 3:
            self.declare(Fact(power = "bad"))

    @Rule(Fact(action = "pitching"), 
    NOT(Fact(power = W())), 
    NOT(Fact(pitcher_position = "CP"),
    Fact(pitcher_position = MATCH.pitcher_position), 
    TEST(lambda pitcher_position: pitcher_position == "SP")))
    def innings_thrown(self):
        self.thrown = input("How many innings has the pitcher thrown today (0-8)? \n")
        self.thrown = int(self.thrown)

        if self.thrown <= 2:
            self.declare(Fact(power = "good"))
        elif self.thrown <= 4:
            self.declare(Fact(power = "fair"))
        elif self.thrown <= 8:
            self.declare(Fact(power = "bad"))
    
    @Rule(Fact(action = "pitching"), Fact(pitching_accuracy = MATCH.pitching_accuracy),
    TEST(lambda pitching_accuracy : pitching_accuracy >= 5))
    def pitching_accurately_1(self):
        self.declare(Fact(pitching_accurately = "yes"))
    
    @Rule(Fact(action = "pitching"), Fact(pitching_accuracy = MATCH.pitching_accuracy),
    TEST(lambda pitching_accuracy : pitching_accuracy < 5))
    def pitching_accurately_2(self):
        self.declare(Fact(pitching_accurately = "no"))

    @Rule(Fact(action = "pitching"), 
    Fact(our_scored = MATCH.our_scored), 
    Fact(rival_scored = MATCH.rival_scored),
    TEST(lambda our_scored, rival_scored : our_scored > rival_scored))
    def lead(self):
        self.declare(Fact(lead = "yes"))
    
    @Rule(Fact(action = "pitching"), 
    Fact(our_scored = MATCH.our_scored), 
    Fact(rival_scored = MATCH.rival_scored),
    TEST(lambda our_scored, rival_scored : our_scored < rival_scored))
    def lead(self):
        self.declare(Fact(lead = "no"))

'''
    @Rule(Fact(action = "pitching"),Fact(pitching = MATCH.pitching))
    def getPitching(self, pitching):
        print(pitching)
        if pitching == "4Seam1":
            print("Pitch a 4-seam fastball at the knees! Since the count is 0-0 and it's late in the game, the run difference really matters. " 
            "In this case you are losing, and since the batter is lower in the lineup, you will be able to blow a fast pitch by him, "
            "which doesn't risk a wild pitch advancing a runner.")
        if pitching == "Changeup1":
            print("Pitch a changeup! Since the count is 0-0 and it's late "
            "in the game, the run difference really matters. In this case you are losing, "
            "and since the batter is lower in the lineup, it is OK to risk a wild pitch "
            "given that there aren't any runners on base.")
'''

if __name__ == "__main__":
    engine = PitchingStrategy()
    while True:
        engine.reset()
        engine.run()
        print("Would you like to diagnose some other symptoms? (yes/no)")
        if input() == "no":
            exit()