from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]

A, B, C = "A", "B", "C"

def rules_for_person(name = str, phrase = None):
    #Returns basic rules for a person
    characters_for_name = []
    for symbol in symbols:
        if str(symbol).startswith(name):
            characters_for_name.append(symbol)
        
    #characters_for_name[0] will be knight [1] will be knave
    rules = And(
        Or(characters_for_name[0], characters_for_name[1]),
        Not(And(characters_for_name[0], characters_for_name[1])),
    )
    if phrase != None:
        rules = And(
            rules,
            And(
        Implication(characters_for_name[0], phrase),
        Implication(characters_for_name[1], Not(phrase)) 
            )                   
        )
        
    return rules

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = rules_for_person(A, And(AKnave, AKnight)) 

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

knowledge1 = And(
    rules_for_person(A, And(AKnave, BKnave)),
    rules_for_person(B)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    rules_for_person(A, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    rules_for_person(B, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)
       
# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    rules_for_person(A, Or(AKnave, AKnight)), 
    rules_for_person(B, And(rules_for_person(A, AKnave), CKnave)),
    rules_for_person(C, AKnight)
)

def main():
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
