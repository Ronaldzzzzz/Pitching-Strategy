from experta import *
import json

pitching_result = {}

class PitchingStrategy(KnowledgeEngine):
    @DefFacts()
    def start(self):

        global pitching_result
        with open('result.json') as f:
            pitching_result = json.load(f)

        print("\nHello! This is an expert system that to help you to select the pitching strategy based on the situation!")
        print("I will ask you a few questions about this plate appearance. And then I will also tell you where/how you should pitch.\n\n")
        yield Fact(action = "pitching")

    # ---------------- Facts ---------------- 

    @Rule(Fact(action = "pitching"), NOT(Fact(runner_1 = W())), salience = 100)
    def runner_at_1(self):
        self.runner_1 = input("Is there a runner on 1B (yes/no)? \n")
        self.declare(Fact(runner_1 = self.runner_1.lower()))
    
    @Rule(Fact(action = "pitching"), NOT(Fact(runner_2 = W())), salience = 99)
    def runner_at_2(self):
        self.runner_2 = input("Is there a runner on 2B (yes/no)? \n")
        self.declare(Fact(runner_2 = self.runner_2.lower()))
    
    @Rule(Fact(action = "pitching"), NOT(Fact(runner_3 = W())), salience = 98)
    def runner_at_3(self):
        self.runner_3 = input("Is there a runner on 3B (yes/no)? \n")
        self.declare(Fact(runner_3 = self.runner_3.lower()))

    @Rule(Fact(action = "pitching"), NOT(Fact(strikes = W())), salience = 97)
    def num_of_strikes(self):
        self.strikes = int(input("How many strikes are there (0-2)? \n"))
        self.declare(Fact(strikes = self.strikes))

    @Rule(Fact(action = "pitching"), NOT(Fact(balls = W())), salience = 96)
    def num_of_balls(self):
        self.balls = int(input("How many balls are there (0-3)? \n"))
        self.declare(Fact(balls = self.balls))
    
    @Rule(Fact(action = "pitching"), NOT(Fact(outs = W())), salience = 95)
    def num_of_outs(self):
        self.outs = input("How many outs are there in this inning(0-2)? \n")
        self.declare(Fact(outs = self.outs))

    @Rule(Fact(action = "pitching"), NOT(Fact(our_scored = W())), salience = 94)
    def num_of_our_scored(self):
        self.our_scored = int(input("How many runs has YOUR TEAM scored ? \n"))
        self.declare(Fact(our_scored = self.our_scored))
    
    @Rule(Fact(action = "pitching"), NOT(Fact(rival_scored = W())), salience = 93)
    def num_of_rival_scored(self):
        self.rival_scored = int(input("How many runs has the RIVAL TEAM scored ? \n"))
        self.declare(Fact(rival_scored = self.rival_scored))

    @Rule(Fact(action = "pitching"), NOT(Fact(batter_order = W())), salience = 92)
    def batter_order(self):
        self.batter_order = int(input("What spot is the batter in the lineup (1-9)? \n"))
        self.declare(Fact(batter_order = self.batter_order))

    @Rule(Fact(action = "pitching"), NOT(Fact(batter_chased = W())), salience = 91)
    def has_batter_chased(self):
        self.batter_chased = input("Has the batter chased one of the last pitches outside the strike zone (yes/no)? \n")
        self.declare(Fact(batter_chased = self.batter_chased.lower()))

    @Rule(Fact(action = "pitching"), NOT(Fact(pitching_accuracy = W())), salience = 90)
    def pitching_accuracy(self):
        self.pitching_accuracy = int(input("On a scale of 1-10, 10 being very accurate, how accurately is the pitcher throwing (1-10)? \n"))
        self.declare(Fact(pitching_accuracy = self.pitching_accuracy))

    @Rule(Fact(action = "pitching"), NOT(Fact(late_innings = W())), salience = 89)
    def innings_now(self):
        self.innings = int(input("What inning is it (0-9)? \n"))
        if self.innings < 7:
            self.declare(Fact(late_innings = "no"))
        else:
            self.declare(Fact(late_innings = "yes"))
    
    @Rule(Fact(action = "pitching"), NOT(Fact(pitcher_position = W())), salience = 88)
    def p_position(self):
        self.pitcher_position = input("What is the position of the pitcher (SP, RP, CP)? \n")
        self.declare(Fact(pitcher_position = self.pitcher_position))
    
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
    TEST(lambda pitcher_position: pitcher_position == "RP")), salience = 87)
    def innings_thrown_1(self):
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
    TEST(lambda pitcher_position: pitcher_position == "SP")), salience = 87)
    def innings_thrown_2(self):
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
    def lead_1(self):
        self.declare(Fact(lead = "yes"))
    
    @Rule(Fact(action = "pitching"), 
    Fact(our_scored = MATCH.our_scored), 
    Fact(rival_scored = MATCH.rival_scored),
    TEST(lambda our_scored, rival_scored : our_scored <= rival_scored))
    def lead_2(self):
        self.declare(Fact(lead = "no"))

    @Rule(Fact(action = "pitching"), 
    Fact(batter_order = MATCH.batter_order),
    TEST(lambda batter_order : batter_order <= 5))
    def front_order_1(self):
        self.declare(Fact(front_order = "yes"))

    @Rule(Fact(action = "pitching"), 
    Fact(batter_order = MATCH.batter_order),
    TEST(lambda batter_order : batter_order > 5))
    def front_order_2(self):
        self.declare(Fact(front_order = "no"))

    # ---------------- Pitching ----------------
    '''
    Type : 
        1: 4-Seam Fastball
        2: 2-Seam Fastball or Sinker
        3: Curveball or Forkball
        4: Changeups or Splitters
        5: Slider or Cutter
    Zoom :
        inside or outside
    Position :
        high or low
    Description :

    Facts:
    strikes: 0~2
    balls: 0~3
    outs: 0~2
    late_innings : yes/no
    front_order: yes/ no.
    batter_chased : yes into.
    scoring_position: yes/no
    lead : yes/no.
    pitching_accurately : yes/no
    power : good/fair/bad
    pitcher_position: SP/RP/CP
    '''
    
    ## ---------------- Type 1 ----------------
    
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0), 
        Fact(strikes = 0),
        Fact(late_innings = "yes"),
        Fact(lead = "no"),
        Fact(batter_chased = "no"), 
        Fact(front_order = "yes"))
    def pitching_1(self):
        self.declare(Fact(pitching = "4Seam_1"))
    
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0), 
        Fact(strikes = 0),
        Fact(scoring_position = "yes"),
        Fact(late_innings = "yes"),
        Fact(lead = "no"),
        Fact(batter_chased = "no"), 
        Fact(front_order = "no"))
    def pitching_2(self):
        self.declare(Fact(pitching = "4Seam_2"))

    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0), 
        Fact(strikes = 0),
        Fact(late_innings = "no"),
        Fact(lead = "no"),
        Fact(batter_chased = "no"))
    def pitching_3(self):
        self.declare(Fact(pitching = "4Seam_3"))
    
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0), 
        Fact(strikes = 0),
        Fact(late_innings = "no"),
        Fact(lead = "no"),
        Fact(batter_chased = "yes"))
    def pitching_4(self):
        self.declare(Fact(pitching = "4Seam_4"))

    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0), 
        Fact(strikes = 1),
        Fact(pitching_accurately = "no"))
    def pitching_5(self):
        self.declare(Fact(pitching = "4Seam_5"))

    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)), 
        Fact(strikes = 2),
        Fact(lead = "yes"),
        Fact(power = "good"))
    def pitching_6(self):
        self.declare(Fact(pitching = "4Seam_6"))

    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)), 
        Fact(strikes = 2),
        Fact(lead = "yes"),
        Fact(power = "fair"),
        Fact(pitching_accurately = "no"))
    def pitching_7(self):
        self.declare(Fact(pitching = "4Seam_7"))

    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)), 
        Fact(strikes = 2),
        Fact(lead = "no"))
    def pitching_8(self):
        self.declare(Fact(pitching = "4Seam_8"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)), 
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(batter_chased = "yes"),
        Fact(scoring_position = "yes"),
        Fact(pitching_accurately = "no"))
    def pitching_9(self):
        self.declare(Fact(pitching = "4Seam_9"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)), 
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"))
    def pitching_10(self):
        self.declare(Fact(pitching = "4Seam_10"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)), 
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(batter_chased = "no"),
        Fact(front_order = "yes"),
        Fact(pitching_accurately = "no"))
    def pitching_11(self):
        self.declare(Fact(pitching = "4Seam_11"))
    
    '''
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)), 
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(batter_chased = "no"),
        Fact(front_order = "no"),
        Fact(pitching_accurately = "no"))
    def pitching_12(self):
        self.declare(Fact(pitching = "4Seam_12"))
    '''
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)), 
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(batter_chased = "no"),
        Fact(front_order = "no"),
        Fact(pitching_accurately = "no"))
    def pitching_13(self):
        self.declare(Fact(pitching = "4Seam_13"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 1), Fact(balls = 2)), 
        Fact(strikes = 0))
    def pitching_14(self):
        self.declare(Fact(pitching = "4Seam_14"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 1), Fact(balls = 2)), 
        Fact(strikes = 1),
        Fact(scoring_position = "yes"),
        Fact(batter_chased = "no"))
    def pitching_15(self):
        self.declare(Fact(pitching = "4Seam_15"))
    
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 3), 
        Fact(strikes = 2),
        Fact(lead = "no"),
        Fact(front_order = "yes"))
    def pitching_16(self):
        self.declare(Fact(pitching = "4Seam_16"))
    
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 3),
        OR(Fact(strikes = 0), Fact(strikes = 1)))
    def pitching_18(self):
        self.declare(Fact(pitching = "4Seam_18"))
    # --------------------------------

    # ---------------- Type 2 ----------------

    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0),
        Fact(strikes = 0),
        Fact(lead = "yes"),
        Fact(late_innings = "yes"))
    def pitching_19(self):
        self.declare(Fact(pitching = "2Seam_1"))
    
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0),
        Fact(strikes = 1),
        Fact(pitching_accurately = "yes"),
        Fact(batter_chased = "no"),
        Fact(front_order = "no"))
    def pitching_20(self):
        self.declare(Fact(pitching = "2Seam_2"))

    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(pitching_accurately = "yes"),
        Fact(batter_chased = "yes"),
        Fact(scoring_position = "yes"))
    def pitching_21(self):
        self.declare(Fact(pitching = "2Seam_3"))

    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(pitching_accurately = "yes"),
        Fact(batter_chased = "no"),
        Fact(front_order = "yes"))
    def pitching_22(self):
        self.declare(Fact(pitching = "2Seam_4"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(batter_chased = "no"),
        Fact(front_order = "no"),
        Fact(pitching_accurately = "yes"))
    def pitching_23(self):
        self.declare(Fact(pitching = "2Seam_5"))

    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 1),
        Fact(scoring_position = "yes"),
        Fact(batter_chased = "yes"))
    def pitching_24(self):
        self.declare(Fact(pitching = "2Seam_6"))
    
    # --------------------------------

    # ---------------- Type 3 ----------------

    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0),
        Fact(strikes = 0),
        Fact(late_innings = "yes"),
        Fact(lead = "no"))
    def pitching_25(self):
        self.declare(Fact(pitching = "Curv_1"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(batter_chased = "yes"),
        Fact(scoring_position = "no"),
        Fact(pitching_accurately = "no"))
    def pitching_26(self):
        self.declare(Fact(pitching = "Curv_2"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(batter_chased = "no"),
        Fact(front_order = "no"),
        Fact(pitching_accurately = "yes"))
    def pitching_27(self):
        self.declare(Fact(pitching = "Curv_3"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 1),
        Fact(scoring_position = "no"))
    def pitching_28(self):
        self.declare(Fact(pitching = "Curv_4"))

    # --------------------------------

    # ---------------- Type 4 ----------------

    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0),
        Fact(strikes = 0),
        Fact(late_innings = "yes"),
        Fact(lead = "no"),
        Fact(front_order = "no"),
        Fact(scoring_position = "no"))
    def pitching_29(self):
        self.declare(Fact(pitching = "Changeup_1"))
    
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0),
        Fact(strikes = 0),
        Fact(late_innings = "no"),
        Fact(lead = "yes"),
        Fact(front_order = "no"))
    def pitching_30(self):
        self.declare(Fact(pitching = "Changeup_2"))

    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 2),
        Fact(late_innings = "no"),
        Fact(lead = "yes"),
        Fact(batter_chased = "yes"),
        Fact(pitching_accurately = "yes"),
        Fact(scoring_position = "no"))
    def pitching_31(self):
        self.declare(Fact(pitching = "Changeup_3"))
    
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 3),
        Fact(strikes = 2),
        Fact(lead = "yes"),
        Fact(pitching_accurately = "no"))
    def pitching_32(self):
        self.declare(Fact(pitching = "Changeup_4"))
    
    # --------------------------------

    # ---------------- Type 4 ----------------

    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0),
        Fact(strikes = 0),
        Fact(late_innings = "no"),
        Fact(lead = "yes"),
        Fact(front_order = "yes"))
    def pitching_33(self):
        self.declare(Fact(pitching = "Cutter_1"))
    
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0),
        Fact(strikes = 1),
        Fact(front_order = "yes"),
        Fact(batter_chased = "no"),
        Fact(pitching_accurately = "yes"))
    def pitching_34(self):
        self.declare(Fact(pitching = "Cutter_2"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(front_order = "no"),
        Fact(batter_chased = "no"),
        Fact(pitching_accurately = "yes"))
    def pitching_35(self):
        self.declare(Fact(pitching = "Cutter_3"))
    
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 3),
        Fact(strikes = 2),
        Fact(lead = "yes"),
        Fact(pitching_accurately = "yes"))
    def pitching_36(self):
        self.declare(Fact(pitching = "Cutter_4"))
    
    # --------------------------------

    # ---------------- Type 5 ----------------
    @Rule(Fact(action = "pitching"), 
        Fact(balls = 0),
        Fact(strikes = 1),
        Fact(batter_chased = "yes"),
        Fact(pitching_accurately = "yes"))
    def pitching_38(self):
        self.declare(Fact(pitching = "Slider_1"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 2),
        Fact(lead = "yes"),
        Fact(power = "fair"),
        Fact(pitching_accurately = "yes"))
    def pitching_37(self):
        self.declare(Fact(pitching = "Slider_2"))
    
    @Rule(Fact(action = "pitching"), 
        OR(Fact(balls = 0), Fact(balls = 1), Fact(balls = 2)),
        Fact(strikes = 2),
        Fact(late_innings = "yes"),
        Fact(lead = "yes"),
        Fact(batter_chased = "no"),
        Fact(front_order = "no"),
        Fact(pitching_accurately = "yes"))
    def pitching_39(self):
        self.declare(Fact(pitching = "Slider_3"))
    # --------------------------------

    # ---------------- Results ---------------- 

    @Rule(Fact(action = "pitching"),Fact(pitching = MATCH.pitching))
    def getPitching(self, pitching):
        global pitching_result
        print(pitching)
        print(pitching_result[pitching])
        


if __name__ == "__main__":
    engine = PitchingStrategy()
    while True:
        engine.reset()
        engine.run()
        print(engine.facts)
        print("Would you still like to use the system? (yes/no)")
        if input() == "no":
            exit()
        '''
        print("would you need me to keep some information? (yes/no)")
        if input() == "no":
            continue
        else:
            print("Which information suould I keep?")
            print("")
        '''
