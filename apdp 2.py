from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Domain Model
# =========================
class Book:
    def __init__(self, title, author, year, language, publisher, isbn):
        self.title = title
        self.author = author
        self.year = year
        self.language = language
        self.publisher = publisher
        self.isbn = isbn


# =========================
# Repository Abstraction
# =========================
class IDataRepository(ABC):
    @abstractmethod
    def load_data(self):
        pass


class CSVBookRepository(IDataRepository):
    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        return pd.read_csv(self.filename)


# =========================
# Service Layer
# =========================
class BookService:
    def __init__(self, repository: IDataRepository):
        self.repository = repository

    def get_books_dataframe(self):
        return self.repository.load_data()


# =========================
# Strategy Abstraction
# =========================
class AnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, df):
        pass


# =========================
# Concrete Strategies
# =========================
class BooksPerYearAnalysis(AnalysisStrategy):
    def analyze(self, df):
        result = df.groupby("publication date")["book"].count()
        print(result)

        plt.plot(result.index, result.values)
        plt.xlabel("Year")
        plt.ylabel("Books")
        plt.title("Books Published Per Year")
        plt.show()


class TopAuthorsAnalysis(AnalysisStrategy):
    def analyze(self, df):
        result = df.groupby("author").size().nlargest(5)
        print(result)

        result.plot(kind="barh")
        plt.title("Top 5 Authors")
        plt.show()


class LanguageDistributionAnalysis(AnalysisStrategy):
    def analyze(self, df):
        result = df.groupby("language").size()
        print(result)

        result.plot(kind="bar")
        plt.title("Books by Language")
        plt.show()


class PublisherAnalysis(AnalysisStrategy):
    def analyze(self, df):
        result = df.groupby("book publisher").size().nlargest(15)
        print(result)

        result.plot(kind="bar")
        plt.title("Top Publishers")
        plt.xticks(rotation=90)
        plt.show()


class MissingISBNAnalysis(AnalysisStrategy):
    def analyze(self, df):
        missing = df["ISBN"].isnull().sum()
        present = df["ISBN"].notnull().sum()

        print(f"Missing ISBN: {missing}")
        print(f"Percentage missing: {(missing/len(df))*100:.2f}%")

        plt.pie([missing, present], labels=["Missing", "Present"], autopct="%1.1f%%")
        plt.title("ISBN Availability")
        plt.show()


class YearlyLanguageAnalysis(AnalysisStrategy):
    def analyze(self, df):
        result = df.groupby(["publication date", "language"]).size().unstack(fill_value=0)
        print(result)

        result.plot()
        plt.title("Books Per Year by Language")
        plt.show()


# =========================
# Strategy Context
# =========================
class AnalysisContext:
    def __init__(self, strategy: AnalysisStrategy):
        self.strategy = strategy

    def execute(self, df):
        self.strategy.analyze(df)


# =========================
# Controller (CLI Layer)
# =========================
class CLIController:
    def __init__(self, service: BookService):
        self.service = service

    def run(self):
        while True:
            print("\n--- Dream Book Shop ---")
            print("1. Books per Year")
            print("2. Top 5 Authors")
            print("3. Books by Language")
            print("4. Books by Publisher")
            print("5. Missing ISBN Analysis")
            print("6. Yearly Books by Language")
            print("7. Exit")

            choice = input("Choose: ")

            df = self.service.get_books_dataframe()

            if choice == "1":
                AnalysisContext(BooksPerYearAnalysis()).execute(df)
            elif choice == "2":
                AnalysisContext(TopAuthorsAnalysis()).execute(df)
            elif choice == "3":
                AnalysisContext(LanguageDistributionAnalysis()).execute(df)
            elif choice == "4":
                AnalysisContext(PublisherAnalysis()).execute(df)
            elif choice == "5":
                AnalysisContext(MissingISBNAnalysis()).execute(df)
            elif choice == "6":
                AnalysisContext(YearlyLanguageAnalysis()).execute(df)
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice")


# =========================
# Program Entry Point
# =========================
if __name__ == "__main__":
    repo = CSVBookRepository("DatasetBooks.csv")
    service = BookService(repo)
    controller = CLIController(service)
    controller.run()
