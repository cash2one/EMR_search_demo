import sys

class TextFeature:
    def __init__(self):
        pass

    def list2dict(self, x):
        d = {}
        for w in x:
            if w not in d:
                d[w] = 0
            d[w] += 1

        return d
                

    def cqr(self, query, doc, term_weight, default_weight):
        q_dict = self.list2dict(query)
        d_dict = self.list2dict(doc)
        total_weight = 0.0
        hit_weight = 0.0
        for t in query:
            if t in term_weight:
                w = term_weight[t]
            else:
                w = default_weight
            total_weight += w
            if t in d_dict:
                hit_weight += w

        if total_weight == 0:
            return 0
        else:
            return hit_weight / total_weight

    def ctr(self, query, doc, term_weight):
        return self.cqr(doc, query, term_weight)

    def bm25(self, query, doc):
        k1 = 2
        b = 0.75
        avgdl = 30
        Kq = k1 * (1 - b + b * len(query) / avgdl)
        Kd = k1 * (1 - b + b * len(doc) / avgdl)
        q_dict = self.list2dict(query)
        d_dict = self.list2dict(doc)
        bm25_score = 0.0
        for t in q_dict:
            if t not in d_dict:
                continue
            qf = q_dict[t]
            f = d_dict[t]
            bm25_score += (f * (k1 + 1) / (f + Kd)) * (qf * (k1 + 1) / (qf + Kq))
            
        return bm25_score
        
        
