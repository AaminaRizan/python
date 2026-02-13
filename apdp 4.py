import pandas as pd
import matplotlib.pyplot as plt


class CSVBookRepository:
    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        return pd.read_csv(self.filename)


class BookService:
    def __init__(self, repository):
        self.repository = repository

    def get_books_dataframe(self):
        return self.repository.load_data()


class TopAuthorsAnalysis:
    def analyze(self, df):
        result = df.groupby("author").size().sort_values(ascending=False).head(5)

        print(result)

        plt.figure()
        ax = result.plot(kind="bar")
        plt.title("Top 5 Most Prolific Authors")
        plt.xlabel("Author")
        plt.ylabel("Number of Books")
        plt.xticks(rotation=30)
        plt.grid(axis="y", linestyle="--", alpha=0.6)

        for bar in ax.patches:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                int(bar.get_height()),
                ha="center",
                va="bottom"
            )

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    repo = CSVBookRepository("DatasetBooks.csv")
    service = BookService(repo)
    df = service.get_books_dataframe()

    analysis = TopAuthorsAnalysis()
    analysis.analyze(df)
