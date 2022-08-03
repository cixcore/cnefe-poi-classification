import clavier
import metaphoneptbr


class WordDistanceMeasurer:
    def __init__(self):
        self.keyboard = clavier.load_qwerty()

    @staticmethod
    def sanitize(sentence):
        return sentence.replace("0", "o").replace("1", "i").replace("3", "e")

    def string_to_list(self, x):
        # print(self.sanitize(x).split())
        return self.sanitize(x).split()

    def has_any_similar_char_seq(self, list_of_words, x):
        return self.match_with_levenshtein_distance(list_of_words, x, 2)

    def match_with_levenshtein_distance(self, list_of_words, x, dist):
        for word_in_description in self.string_to_list(x):
            for word in list_of_words:
                # print(f'word: "{word}" | word from descr: "{word_in_description}".')
                if self.keyboard.word_distance(word, word_in_description) <= dist:
                    return True
        return False

    def has_any_similar_phonetic_word(self, list_of_words, x):
        for word_in_description in self.string_to_list(x):
            for word in list_of_words:
                if metaphoneptbr.phonetic(word) == metaphoneptbr.phonetic(word_in_description):
                    return True
        return False

    def test_dists(self):
        print(self.keyboard.word_distance("lancha", "lanche"))
        print(self.keyboard.word_distance("lancho", "lanchi"))
        print(self.keyboard.word_distance("lancho", "lancha"))
        print(self.keyboard.word_distance("pneu", "pneus"))
        print(self.keyboard.word_distance("barcaca", "barcassa"))
        print(self.keyboard.word_distance("metalurgia", "metalurgica"))
        print(metaphoneptbr.phonetic("xiqueiro"))
        print(metaphoneptbr.phonetic("chiqueiro"))
        print(metaphoneptbr.phonetic("escritorio"))
        print(metaphoneptbr.phonetic("escrotorio"))
        print(metaphoneptbr.phonetic("barcaca"))
        print(metaphoneptbr.phonetic("barcassa"))


dists = WordDistanceMeasurer()
