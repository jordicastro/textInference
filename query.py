import sys
from utils import load_successor_map, query_inference

def main() -> str:
    ngram = 2
    num_prediction_words = 50
    context = "some cupid kills with arrows some"
    if len(sys.argv) == 4:
        ngram = int(sys.argv[1])
        num_prediction_words = int(sys.argv[2])
        context = sys.argv[3]

    if len(context) < ngram - 1:
        print("ERROR: context is too short for the n-gram model")
        return "ERROR: context is too short for the n-gram model"
    else:
        successor_map = load_successor_map(ngram, debug=False)
        result:str = query_inference(successor_map, ngram, num_prediction_words, context)
        print(result)
        return result
        
if __name__ == "__main__":
    main()