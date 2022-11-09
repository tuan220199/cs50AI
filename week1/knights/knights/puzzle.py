from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")





# Puzzle 0
# A says "I am both a knight and a knave."
sentenceA = And(AKnight,AKnave)
knowledge0 = And(
    # TODO
    Not(And(AKnave,AKnight)),
    Or(AKnight,AKnave),
    Biconditional(sentenceA,AKnight),
    Biconditional(sentenceA,Not(AKnave))
)

# Puzzle 1
# A says "We are both knaves."
sentenceA = And(AKnave,BKnave)
# B says nothing.
knowledge1 = And(
    # TODO
    Not(And(AKnave,AKnight)),
    Not(And(BKnave,BKnight)),
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Biconditional(sentenceA,AKnight),
    Biconditional(sentenceA,Not(AKnave))
)

# Puzzle 2
# A says "We are the same kind."
sentenceA = Or(
    And(AKnight,BKnight),
    And(AKnave,BKnave)
    )
# B says "We are of different kinds."
sentenceB = Or(
    And(AKnight,BKnave),
    And(AKnave,BKnight)
    )
knowledge2 = And(
    # TODO
    Not(And(AKnave,AKnight)),
    Not(And(BKnave,BKnight)),
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Biconditional(sentenceA,AKnight),
    Biconditional(sentenceA,Not(AKnave)),
    Biconditional(sentenceB,BKnight),
    Biconditional(sentenceB,Not(BKnave)),        
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
sentenceA = Or(
    And(Not(AKnight),AKnave),
    And(Not(AKnave),AKnight)
    )
# B says "A said 'I am a knave'."
sentenceB = And(
    sentenceA,
    AKnave
    )
# B says "C is a knave."
sentenceB.add(
    CKnave
    )
# C says "A is a knight."
sentenceC = AKnight
knowledge3 = And(
    # TODO
    Not(And(AKnave,AKnight)),
    Not(And(BKnave,BKnight)),
    Not(And(CKnave,CKnight)),
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Or(CKnight,CKnave),
    Biconditional(sentenceA,AKnight),
    Biconditional(sentenceA,Not(AKnave)),
    Biconditional(sentenceB,BKnight),
    Biconditional(sentenceB,Not(BKnave)),
    Biconditional(sentenceC,CKnight),
    Biconditional(sentenceC,Not(CKnave)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
