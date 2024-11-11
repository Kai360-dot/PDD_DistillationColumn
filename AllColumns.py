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
pressure = 5
print(f'Pressure: {pressure} bar')
column_manager = ColumnManager(pressure)
column_manager.add_column('k1', ['A'], ['B', 'C', 'D'])
column_manager.add_column('k2', ['A', 'B'], ['C', 'D'])
column_manager.add_column('k3', ['A', 'B', 'C'], ['D'])
column_manager.add_column('k4', ['A'], ['B', 'C'])
column_manager.add_column('k5', ['A', 'B'], ['C'])
column_manager.add_column('k6', ['B'], ['C', 'D'])
column_manager.add_column('k7', ['B', 'C'], ['D'])
column_manager.add_column('k8', ['A'], ['B'])
column_manager.add_column('k9', ['B'], ['C'])
column_manager.add_column('k10', ['C'], ['D'])

# Print data for all columns
column_manager.print_all_columns_data()


# print('Condenser rel Heat D:')
# for column_name, column_obj in column_manager.columns.items():
#     print(f'{column_name} = {(column_obj.relative_duty_condenser):.3f},')

# print('Reboiler rel Heat D:')
# for column_name, column_obj in column_manager.columns.items():
#     print(f'{column_name} = {(column_obj.relative_duty_reboiler):.3f},')

# print('Temperature Difference:')
# for column_name, column_obj in column_manager.columns.items():
#     print(f'{column_name} = {(column_obj.Temperature_difference):.3f},')
