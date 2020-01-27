from tkinter import filedialog
import reportlab
def save_as():
	filename = filedialog.asksaveasfilename(initialdir=".", title="Save PDF",
												 filetypes=(("PDF files", "*.pdf")))
	return filename

def calc_conformity(list_of_lists):
	for i,l in enumerate(list_of_lists):
		if i>0:
			if l[2] == "ERREUR":
				list_of_lists[i][-1] = "NOK"
			else:
				diff = float(l[2])-float(l[3])
				list_of_lists[i][4] = str(diff)
				if abs(diff) <= float(l[5]):
					list_of_lists[i][-1] = "OK"
				else:
					list_of_lists[i][-1] = "NOK"

def generate_pdf(txt_file):
	file = open(txt_file,'r')
	print("filename:",txt_file)
	lines_list = file.readlines()
	lines_data = []
	for l in lines_list:
		if not l.strip():
			continue
		else:
			lines_data.append(l.split())
	# print(lines_data)
	calc_conformity(lines_data)
# FONCTION - CALIBRE - APPAREIL - ETALON - ECART - EMT - INCERTITUDE - CONFORMITE
# VDC 50 _MV  # 25.0    -25.0  remplir    remplir   NOK

	for i,l in enumerate(lines_data):
		if '_' in l[0]:
			lines_data[i][0] = l[0].replace('_',' ')+" Hz"
	for i,l in enumerate(lines_data):
		if i > 0:
			# print("bef",l[1])
			tmp = l[1].split('_')
			# print("tmp",tmp)
			# print(l)
			if len(tmp[1]) == 2:
				formatted = tmp[1][0].lower() + tmp[1][1]
				lines_data[i][1] = tmp[0]+" "+formatted
				# print(lines_data[i])
			else:
				lines_data[i][1] = lines_data[i][1].replace('_',' ')
	for i,l in enumerate(lines_data):
		if i > 0:
			if 'O' in l[1]:
				lines_data[i][1] = l[1].replace('O','\u03A9')
				print(l[1])
			if 'm' in l[1] and l[0]=="R":
				print("entrou m",l[1])
				lines_data[i][1] = l[1].replace('m','M')


	filename = txt_file.replace("txt","pdf")

	from reportlab.platypus import SimpleDocTemplate
	from reportlab.lib.pagesizes import letter, A4, portrait
	from reportlab.platypus import Table, TableStyle
	from reportlab.lib import colors
	style = TableStyle()
	pdf = SimpleDocTemplate(filename, pagesize=letter)
	pdf_elements = []
	# print(lines_data[0][0])
	lines_data[0]= lines_data[0][0].split('-')
	# print(lines_data)

	style = TableStyle([
		('BACKGROUND', (0, 0), (7, 0), colors.lightgreen),
		('ALIGN', (0, 0), (-1, -1), 'CENTER'),
		('BOX',(0,0),(-1,-1),2,colors.black),
		('GRID', (0, 0), (-1, -1),2, colors.black)

	])
	# for i,l in enumerate(lines_data):
	# 	if l[-1]  == "NOK":
	# 		print("nok")
	# 		bc = colors.red
	# 	elif l[-1]=="OK":
	# 		bc = colors.green
	# 	else:
	# 		continue
	# 	ts = TableStyle(
	# 		[('BACKGROUND', (0, i), bc)]
	# 	)
	# 	table.setStyle(ts)
	for row, values, in enumerate(lines_data):
		for column, value in enumerate(values):
			# print(value)
			if value == "NOK":
				style.add('BACKGROUND', (column, row), (column, row), colors.red)
			elif value == "OK":
				style.add('BACKGROUND', (column, row), (column, row), colors.green)
			elif '.' in value:
				lines_data[row][column] = value.replace('.', ',')
			elif "AC" in value:
				style.add('BACKGROUND',(column,row),(-1,row),colors.lightgrey)
			else:
				continue
	table = Table(lines_data)
	table.setStyle(style)
	pdf_elements.append(table)
	pdf.build(pdf_elements)

generate_pdf("C:\\Users\\João Marcos Costa\\Documents\\ENSICAEN2019-2020\\Projet Industriel\\dev\\CA5277.txt")
