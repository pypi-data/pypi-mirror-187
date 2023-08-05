from river import stream
from river import cluster
from river import metrics

class River:
    def __init__(self, model):
        self.model = model
        self.metric = metrics.cluster.Cohesion()
        
    def partial_fit(self, umap_embeddings):
        for umap_embedding, _ in stream.iter_array(umap_embeddings):
            self.model = self.model.learn_one(umap_embedding)

        labels = []
        for umap_embedding, _ in stream.iter_array(umap_embeddings):
            label = self.model.predict_one(umap_embedding)
            self.metric = self.metric.update(umap_embedding, label, self.model.centers)
            labels.append(label)

        # calculate silhouette at the end of the partial fit
        #self.metric = silhouette_score(umap_embeddings, labels)
        self.labels_ = labels
        return self