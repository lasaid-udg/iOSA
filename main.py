import sys
from PyQt5.QtWidgets import QApplication

from loginWindow import LogInWindow


def main():
    app = QApplication(sys.argv)
    log_in = LogInWindow()
    sys.exit(app.exec_())


def ia_window_test() -> None:
    from iaFilterWidget import iaFiltersWidget

    app = QApplication(sys.argv)
    ia = iaFiltersWidget()
    ia.show()
    sys.exit(app.exec_())


def range_window_test() -> None:
    from rangesDiscretization import RangeDiscretizationWidget

    app = QApplication(sys.argv)
    rng = RangeDiscretizationWidget((True,True,True))
    rng.show()
    sys.exit(app.exec_())


def discretization_test() -> None:
    import pandas as pd
    from IntelligentAnalisys import Discretize

    df = pd.read_csv(r"C:\Users\zaira\Downloads\test_dump.csv")
    dz = Discretize(df)
    # dz.discretize(3)
    dz.predefined_discretize(3)
    dz.transaction_discretize()



if __name__ == '__main__':
    main()
    # ia_window_test()
    # range_window_test()
    # discretization_test()
