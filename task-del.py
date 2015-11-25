from util import *
from openpyxl import *

p = Parser()
# p.create_test_wb(10, 10, 'Sheet1', '../data/A/test.xlsx')
# wb    = p.load_workbook('test.xlsx')
# sheet = wb.get_sheet_by_name('Sheet1')
# p.del_row(sheet, 3)
# wb.save(join(p.path, 'test.xlsx'))

wb    = p.load_workbook('all_data.xlsx')
sheet = wb.get_sheet_by_name('Modified')
ct = 0
for i in range(1413) :
    if str(sheet['K' + str(i+1)].value) == 'Not reported' :
        p.del_row(sheet, i+1)
        print 'delete row' + str(i+1)
        ct += 1
print ct
wb.save(join(p.path, 'all_data.xlsx'))