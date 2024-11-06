from column import Column

class ColumnManager:
    """Defaults to pressure of 1 bar."""
    def __init__(self, pressure = 1):
        self.columns = {}
        self.pressure = pressure

    def add_column(self, name, top_components, bottom_components):
        self.columns[name] = Column(top_components, bottom_components, self.pressure)

    def print_all_columns_data(self):
        for name, column in self.columns.items():
            print(f"Data for {name}:")
            column.print_column_data()
            print("\n")

# Usage
column_manager = ColumnManager()
column_manager.add_column('column_A_BCD', ['A'], ['B', 'C', 'D'])
column_manager.add_column('column_AB_CD', ['A', 'B'], ['C', 'D'])
column_manager.add_column('column_ABC_D', ['A', 'B', 'C'], ['D'])
column_manager.add_column('column_A_BC', ['A'], ['B', 'C'])
column_manager.add_column('column_AB_C', ['A', 'B'], ['C'])
column_manager.add_column('column_B_CD', ['B'], ['C', 'D'])
column_manager.add_column('column_BC_D', ['B', 'C'], ['D'])
column_manager.add_column('column_A_B', ['A'], ['B'])
column_manager.add_column('column_B_C', ['B'], ['C'])
column_manager.add_column('column_C_D', ['C'], ['D'])

# Print data for all columns
# column_manager.print_all_columns_data()
