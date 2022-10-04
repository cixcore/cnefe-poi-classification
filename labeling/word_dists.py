import clavier
import metaphoneptbr


class WordDistanceMeasurer:
    def __init__(self, percentage_change_allowed=0.25):
        self.keyboard = clavier.load_qwerty()
        self.percentage_change_allowed = percentage_change_allowed

    def has_any_similar_char_seq(self, list_of_words, x):
        return self.match_with_levenshtein_distance(list_of_words, x, self.percentage_change_allowed)

    def match_with_levenshtein_distance(self, list_of_words, x, percentage_change_allowed):
        for word_in_description in x.split():
            for word in list_of_words:
                dist = self.keyboard.word_distance(word, word_in_description)
                longest_word_len = max(len(word), len(word_in_description))
                # print(f'word: "{word}" | word from descr: "{word_in_description}" | dist: {dist} | change: {dist/longest_word_len}.')
                if dist/longest_word_len <= percentage_change_allowed:
                    return True
        return False

    @staticmethod
    def has_any_similar_phonetic_word(list_of_words, x):
        for word_in_description in x.split():
            # print(word_in_description)
            for word in list_of_words:
                # print(word)
                # soundex_word = metaphoneptbr.phonetic(word)
                # soundex_word_in_description = metaphoneptbr.phonetic(word_in_description)
                # print(f'word: "{soundex_word}" | word from descr: "{soundex_word_in_description}" | equals: {soundex_word == soundex_word_in_description}.')
                if metaphoneptbr.phonetic(word) == metaphoneptbr.phonetic(word_in_description):
                    return True
        return False

    def test_dists(self):
        fut_dist = self.keyboard.word_distance('construcao', 'contrucao')
        max_len = max(len('construcao'), len('futebol'))
        print(f'futebol-fotebol dist: {fut_dist} '
              f'| max len: {max_len} | percentage: {fut_dist/max_len}')

        ou_dist = self.keyboard.char_distance('l', 'u')
        ie_dist = self.keyboard.char_distance('i', 'e')
        ao_dist = self.keyboard.char_distance('a', 'o')
        ul_dist = self.keyboard.char_distance('u', 'l')
        print(f'o-l: {ou_dist} | i-e: {ie_dist} | a-o: {ao_dist} | u-l: {ul_dist}')

        lanche_dist = self.keyboard.word_distance('lanche', 'lancha')
        max_len = max(len('lanche'), len('lancha'))
        print(f'lanche-lancha dist: {lanche_dist} '
              f'| max len: {max_len} | percentage: {lanche_dist/max_len}')

        ea_dist = self.keyboard.char_distance('a', 'e')
        print(f'a-e: {ea_dist}')

        print(self.keyboard.word_distance("lancha", "lanche"))
        print(self.keyboard.word_distance("lancho", "lanchi"))
        print(self.keyboard.word_distance("lancho", "lancha"))
        print(self.keyboard.word_distance("pneu", "pneus"))
        print(self.keyboard.word_distance("cabelereiro", "cabeleireiro"))
        print(self.keyboard.word_distance("barcaca", "barcassa"))
        print(self.keyboard.word_distance("metalurgia", "metalurgica"))
        print(self.keyboard.word_distance('cabelereiro', 'cabeleireiro') <= 2.0)
        print(metaphoneptbr.phonetic("xiqueiro"))
        print(metaphoneptbr.phonetic("chiqueiro"))
        print(metaphoneptbr.phonetic("xícara"))
        print(metaphoneptbr.phonetic("visão"))
        print(metaphoneptbr.phonetic("vazio"))
        print(metaphoneptbr.phonetic("CABELEIREIRO"))
        print(metaphoneptbr.phonetic("CABELEIRO"))
        print(metaphoneptbr.phonetic("futebol"))
        print(metaphoneptbr.phonetic("fotibau"))
        print(metaphoneptbr.phonetic("escritorio"))
        print(metaphoneptbr.phonetic("escrotorio"))
        print(metaphoneptbr.phonetic("barcaca"))
        print(metaphoneptbr.phonetic("barcassa"))


dists = WordDistanceMeasurer()
dists.test_dists()

