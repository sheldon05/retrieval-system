import numpy as np
from numpy.linalg import norm
from retrieval_system.core.models import Document, Corpus


def calculate_lsi(corpus: Corpus):

    tfidf_matrix, documents = corpus.tf_idf_matrix, corpus.documents.all()
    print("TFIDF MATRIX FOR SVD: ", tfidf_matrix)
    print("SHAPE: ", np.shape(tfidf_matrix))

    A = np.transpose(tfidf_matrix)

    T, S, DT = np.linalg.svd(A, full_matrices=False)

    minimum = min(np.shape(A))
    k = int(minimum * 60 / 100)

    DT = DT[: -(len(DT) - k)]

    # Truncate matrices
    T = T[:, :k]
    S = S[:k]
    S = np.diag(S)

    S = np.linalg.inv(S)
    DT = np.transpose(DT)

    return T, S, DT, documents


def evaluate(query, corpus: Corpus):

    T, S, DT, documents = (
        corpus.t_lsi_matrix,
        corpus.s_lsi_matrix,
        corpus.dt_lsi_matrix,
        corpus.documents.all(),
    )

    T_dot_S_transpose = np.dot(T, S).T

    query_vec = np.transpose(np.dot(T_dot_S_transpose, np.transpose(query)))

    document_ranking = []

    for doc in range(np.shape(DT)[0]):
        doc_vector = DT[doc]
        doc_query_cos = np.dot(query_vec, doc_vector) / (
            norm(query_vec) * norm(doc_vector)
        )
        print(f"Doc {doc} evaluates to {doc_query_cos}")
        document_ranking.append((documents[doc], doc_query_cos))

    document_ranking.sort(key=lambda x: x[1], reverse=True)
    return document_ranking
