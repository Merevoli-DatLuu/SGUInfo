# Ver 1.0
# cào 1 đứa ~ 2s (còn tùy vào server trường)
# Fastscan 100 đứa ~ 75s
# BUG: bị timeout [TimeoutError: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond]
# BUG: lỗi get ngày sinh (do server trường)
# chưa change useragent và ip

from bs4 import BeautifulSoup
import requests
from threading import Thread
import threading
import json
import time

# init color text
red_clr = "\033[91m"
blue_clr = "\033[96m"
green_clr = "\033[92m"
orage_clr = "\033[33m"
lightgreen_clr = "\033[92m"
lightblue_clr = "\033[94m"
reset_clr = "\033[00m"


def print_banner():
	print(blue_clr + "  ___    ___   _   _ " + orage_clr + "  ___           __       " + reset_clr)
	print(blue_clr + " / __|  / __| | | | |" + orage_clr + " |_ _|  _ _    / _|  ___ " + reset_clr)
	print(blue_clr + " \\__ \\ | (_ | | |_| |" + orage_clr + "  | |  | ' \\  |  _| / _ \\ " + reset_clr)
	print(blue_clr + " |___/  \\___|  \\___/ " + orage_clr + " |___| |_||_| |_|   \\___/" + reset_clr)
	print()
	print(green_clr + "  Version: 1.0" + reset_clr)

def print_menu():
	print()
	print(" -- " + green_clr + "MENU" + reset_clr + " -------------------------------")
	print(" | [1] Tìm thông tin sinh viên         |")
	print(" | [2] Quét thông tin sinh viên        |")
	print(" | [3] Quét thông tin bằng file        |")
	print(" | [4] Quét thông tin bằng file (Fast) |")
	print(" |                                     |")
	print(" | [0] Thoát                           |")
	print(" ---------------------------------------")
	print()

def check_mssv(mssv):
	"""
	Kiểm tra xem mssv có hợp lệ hay không
	:param mssv : str
	:return bool
	"""
	if mssv != "":
		res = requests.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=thoikhoabieu&sta=1&id=' + mssv)
		soup = BeautifulSoup(res.text, 'html.parser')
		check_str = soup.findAll('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_lbltieudetkb'})[0].text
		if check_str == 'Thông Tin Thời Khóa Biểu':
			return True
		else:
			return False
	else:
		return False

def check_mssv_option_2(start_mssv, end_mssv):
	"""
	Kiểm tra 2 mã mssv đầu và mssv cuối có hợp lệ hay không
	:param start_mssv : str
	:param end_mssv : str
	:return bool
	"""
	if check_mssv(start_mssv) == True and check_mssv(end_mssv) == True:
		sub = int(end_mssv) - int(start_mssv)
		if sub < 0:
			print(red_clr + "[Lỗi]: Mã cuối bé hơn mã đầu" + reset_clr)
			return False
		elif (sub > 100):
			print(orage_clr + "[Cảnh Báo] Khoảng quét quá lớn có thể bị TimeoutError" + reset_clr)
			return True
		else:
			return True

	else:
		return False

def timthongtin(mssv):
	"""
	Function cho option 1
	Tìm thông tin của 1 sinh viên theo mssv
	Xuất thông tin của sinh viên -> console
	:param mssv : str
	:return None
	"""
	if check_mssv(mssv) == True or check_mssv(mssv) == True:	# check 2 lần -> giảm tỉ lệ sai
		start_time = time.time()
		s = requests.Session()

		# thông tin cơ bản
		data_post = {
			"__EVENTTARGET" : "",
			"__EVENTARGUMENT" : "", 
			"__VIEWSTATE" : "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",
			"__VIEWSTATEGENERATOR" : "CA0B0334",
			"ctl00$ContentPlaceHolder1$ctl00$txtMaSV" : mssv,
			"ctl00$ContentPlaceHolder1$ctl00$btnOK" : "OK"
		}
		s.post("http://thongtindaotao.sgu.edu.vn/default.aspx?page=nhapmasv&flag=XemHocPhi", data = data_post)
		res = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
		soup = BeautifulSoup(res.text, 'html.parser')
		hoten = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblTenSinhVien'}).text
		gioitinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblPhai'}).text
		noisinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblNoiSinh'}).text
		lop = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblLop'}).text
		nganh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lbNganh'}).text
		khoa = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblKhoa'}).text
		hedaotao = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblHeDaoTao'}).text
		khoahoc = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblKhoaHoc'}).text
		covanhoctap = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblCVHT'}).text
		
		# ngày sinh
		r = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=thoikhoabieu&sta=1&id=' + mssv)
		soup = BeautifulSoup(r.text, 'html.parser')
		ngaysinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_lblContentTenSV'}).text.split(':')[1]

		# số điện thoại
		'''res_2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/Report_XemHocPhi.aspx')
		soup = BeautifulSoup(res_2.text, 'html.parser')
		check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
		res_3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str)
		soup = BeautifulSoup(res_3.text, 'html.parser')
		sdt = ""
		td_ls = soup.findAll('td')
		if len(td_ls) > 1275:
			sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
		else:
			for e in td_ls:
				if e.text.split(':')[0] == "Điện thoại":
					sdt = e.text.split(':')[1][1:]
		'''

		# số điện thoại (better)
		sdt = "" #td_ls[305].text
		email = "" #td_ls[258].text

		res_2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/TKBReportView.aspx')
		soup = BeautifulSoup(res_2.text, 'html.parser')
		have_page = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})
		if len(have_page) > 0: # get đc từ in TKB
			check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
			res_3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str)
			soup = BeautifulSoup(res_3.text, 'html.parser')
			td_ls = soup.findAll('td')

			for i in range(len(td_ls)):
				if td_ls[i].text == 'Äiá»n Thoáº¡i':
					sdt = td_ls[i+1].text
				if td_ls[i].text == 'Email :':
					email = td_ls[i+1].text
		else:	# ko có in TKB do sv bảo lưu hoặc rút hồ sơ
			r1 = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
			r2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/Report_XemHocPhi.aspx', timeout = 20)
			soup = BeautifulSoup(r2.text, 'html.parser')
			check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
			r3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str, timeout = 20)
			soup = BeautifulSoup(r3.text, 'html.parser')
			#sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
			sdt = ""
			#test
			td_ls = soup.findAll('td')
			if len(td_ls) > 1275:
				sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
			else:
				for e in td_ls:
					if e.text.split(':')[0] == "Điện thoại":
						sdt = e.text.split(':')[1][1:]

		thongtin = {
			"Mã Số" : mssv,
			"Họ Tên" : hoten,
			"Giới tính" : gioitinh,
			"Ngày sinh" : ngaysinh,
			"Nơi sinh" : noisinh,
			"Lớp" : lop,
			"Ngành" : nganh,
			"Khoa" : khoa,
			"Hệ đào tạo" : hedaotao,
			"Khóa học" : khoahoc,
			"Cố vấn học tập" : covanhoctap,
			"Số điện thoại" : sdt,
			"Email" : email
		}
		
		# print thong tin
		print()
		print("==============" + orage_clr + " Thông Tin " + reset_clr + "==============")
		print(blue_clr + "Mã Số:" + reset_clr, mssv)
		print(blue_clr + "Họ Tên:" + reset_clr, hoten)
		print(blue_clr + "Giới tính:" + reset_clr, gioitinh)
		print(blue_clr + "Ngày sinh:" + reset_clr, ngaysinh)
		print(blue_clr + "Nơi sinh:" + reset_clr, noisinh)
		print(blue_clr + "Lớp:" + reset_clr, lop)
		print(blue_clr + "Ngành:" + reset_clr, nganh)
		print(blue_clr + "Khoa:" + reset_clr, khoa)
		print(blue_clr + "Hệ đào tạo:" + reset_clr, hedaotao)
		print(blue_clr + "Khóa học:" + reset_clr, khoahoc)
		print(blue_clr + "Cố vấn học tập:" + reset_clr, covanhoctap)
		print(blue_clr + "Số điện thoại:" + reset_clr, sdt)
		print(blue_clr + "Email:" + reset_clr, email)
		print("========================================")
		print()
		print((lightgreen_clr + "Time: %.3f s" + reset_clr)%(time.time() - start_time))
		print()

	else:
		print(red_clr + "Mã số sinh viên ko tồn tại!\n" + reset_clr)

def caothongtin(start_mssv, end_mssv):
	"""
	Function cho option 2
	Tìm thông tin nhiều sinh viên từ mssv đầu đến mssv cuối
	Xuất ra thông tin nhiều sinh viên -> console
	:param start_mssv : str
	:param end_mssv : str
	:return None
	"""
	# Cà Mã số sinh viên
	start_time = time.time()
	print(blue_clr + "Đang Tìm những mssv hợp lệ..." + reset_clr)

	mssv = start_mssv
	arr_mssv = []
	while (int(mssv) <= int(end_mssv)):
		#res = requests.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=thoikhoabieu&sta=1&id=' + mssv)
		#soup = BeautifulSoup(res.text, 'html.parser')
		#check_str = soup.findAll('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_lbltieudetkb'})[0].text
		#if (check_str == 'Thông Tin Thời Khóa Biểu'):
		if check_mssv(mssv) == True or check_mssv(mssv) == True:	# check 2 lần -> giảm tỉ lệ sai
			arr_mssv.append(mssv)
			print(green_clr + mssv + reset_clr)
		mssv = str(int(mssv) + 1)

	s = requests.Session()

	number = 1

	print()
	print(green_clr + "Đã tìm thấy", len(arr_mssv), "mssv hợp lệ." + reset_clr)
	print()
	print(blue_clr + "Bắt đầu quét thông tin sinh viên..." + reset_clr)
	# Cà thông tin
	arr_thongtin = []
	for mssv in arr_mssv:
		data_post = {
			"__EVENTTARGET" : "",
			"__EVENTARGUMENT" : "", 
			"__VIEWSTATE" : "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",
			"__VIEWSTATEGENERATOR" : "CA0B0334",
			"ctl00$ContentPlaceHolder1$ctl00$txtMaSV" : mssv,
			"ctl00$ContentPlaceHolder1$ctl00$btnOK" : "OK"
		}
		x = s.post("http://thongtindaotao.sgu.edu.vn/default.aspx?page=nhapmasv&flag=XemHocPhi", data = data_post, timeout = 20)
		res = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
		soup = BeautifulSoup(res.text, 'html.parser')
		hoten = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblTenSinhVien'}).text
		gioitinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblPhai'}).text
		noisinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblNoiSinh'}).text
		lop = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblLop'}).text
		nganh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lbNganh'}).text
		khoa = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblKhoa'}).text
		hedaotao = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblHeDaoTao'}).text
		khoahoc = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblKhoaHoc'}).text
		covanhoctap = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblCVHT'}).text
		
		# ngày sinh
		r = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=thoikhoabieu&sta=1&id=' + mssv)
		soup = BeautifulSoup(r.text, 'html.parser')
		ngaysinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_lblContentTenSV'}).text.split(':')[1]

		# số điện thoại (better)
		sdt = "" #td_ls[305].text
		email = "" #td_ls[258].text

		res_2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/TKBReportView.aspx')
		soup = BeautifulSoup(res_2.text, 'html.parser')
		have_page = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})
		if len(have_page) > 0: # get đc từ in TKB
			check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
			res_3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str)
			soup = BeautifulSoup(res_3.text, 'html.parser')
			td_ls = soup.findAll('td')

			for i in range(len(td_ls)):
				if td_ls[i].text == 'Äiá»n Thoáº¡i':
					sdt = td_ls[i+1].text
				if td_ls[i].text == 'Email :':
					email = td_ls[i+1].text

		else:	# ko có in TKB do sv bảo lưu hoặc rút hồ sơ
			r1 = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
			r2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/Report_XemHocPhi.aspx', timeout = 20)
			soup = BeautifulSoup(r2.text, 'html.parser')
			check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
			r3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str, timeout = 20)
			soup = BeautifulSoup(r3.text, 'html.parser')
			#sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
			sdt = ""
			#test
			td_ls = soup.findAll('td')
			if len(td_ls) > 1275:
				sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
			else:
				for e in td_ls:
					if e.text.split(':')[0] == "Điện thoại":
						sdt = e.text.split(':')[1][1:]

		thongtin = {
			"Mã Số" : mssv,
			"Họ Tên" : hoten,
			"Giới tính" : gioitinh,
			"Ngày sinh" : ngaysinh,
			"Nơi sinh" : noisinh,
			"Lớp" : lop,
			"Ngành" : nganh,
			"Khoa" : khoa,
			"Hệ đào tạo" : hedaotao,
			"Khóa học" : khoahoc,
			"Cố vấn học tập" : covanhoctap,
			"Số điện thoại" : sdt,
			"Email" : email
		}
		
		# làm mới session sau cứ 100 lượt
		#if number%100 == 0:
		#	s = requests.Session()

		# print thong tin
		print()
		print("===" + orage_clr, number, reset_clr + "======================")
		print(blue_clr + "Mã Số:" + reset_clr, mssv)
		print(blue_clr + "Họ Tên:" + reset_clr, hoten)
		print(blue_clr + "Giới tính:" + reset_clr, gioitinh)
		print(blue_clr + "Ngày sinh:" + reset_clr, ngaysinh)
		print(blue_clr + "Nơi sinh:" + reset_clr, noisinh)
		print(blue_clr + "Lớp:" + reset_clr, lop)
		print(blue_clr + "Ngành:" + reset_clr, nganh)
		print(blue_clr + "Khoa:" + reset_clr, khoa)
		print(blue_clr + "Hệ đào tạo:" + reset_clr, hedaotao)
		print(blue_clr + "Khóa học:" + reset_clr, khoahoc)
		print(blue_clr + "Cố vấn học tập:" + reset_clr, covanhoctap)
		print(blue_clr + "Số điện thoại:" + reset_clr, sdt)
		print(blue_clr + "Email:" + reset_clr, email)
		print("========================================")
		print()
		number = number + 1

		arr_thongtin.append(thongtin)

	print()
	print((lightgreen_clr + "Time: %.3f s" + reset_clr)%(time.time() - start_time))
	print()
	print(green_clr + "Hoàn tất quét thông tin!" + reset_clr)

	# Save file
	save_choice = input(orage_clr + "Bạn có muốn lưu thông tin đã quét?" + green_clr + " [Y] -> Yes" + " | Others -> No: " + reset_clr)

	if save_choice == "Y" or save_choice == "y":
		file_choice = input(orage_clr + "Bạn muốn lưu file nào? [1] -> json | [2] -> csv | [3] -> [Both] | [Other] -> [None]: " + reset_clr)

		if file_choice == '1' or file_choice == '3':
			# save to json file
			try:
				with open('datasgu.json', 'w') as out_json_file:
					json.dump(arr_thongtin, out_json_file)
				
				print(green_clr + "Đã lưu thông tin thành công" + reset_clr)
				print(green_clr + "Thông tin được lưu ở ./datasgu.json" + reset_clr)
				#print(green_clr + "Bạn có thể vào trang " + blue_clr + "https://json-csv.com/" + green_clr + " để convert sang file excel" + reset_clr)
			except IOError:
				print(red_clr + "[I/O error] Lưu json file thất bại" + reset_clr)

		if file_choice == '2' or file_choice == '3':
			# save to csv file
			import csv
			csv_columns = ["Mã Số", "Họ Tên", "Giới tính", "Ngày sinh", "Nơi sinh", "Lớp", "Ngành", "Khoa", "Hệ đào tạo", "Khóa học", "Cố vấn học tập", "Số điện thoại", "Email"]
			
			try:
				with open("datasgu.csv", 'w', encoding = 'utf-8-sig', newline='') as out_csv_file:
					writer = csv.DictWriter(out_csv_file, fieldnames=csv_columns)
					writer.writeheader()
					for data in arr_thongtin:
						writer.writerow(data)

				print(green_clr + "Đã lưu thông tin thành công" + reset_clr)
				print(green_clr + "Thông tin được lưu ở ./datasgu.csv" + reset_clr)

			except IOError:
				print(red_clr + "[I/O error] Lưu csv file thất bại" + reset_clr)
		
	print()

def caothongtin_file(file):
	"""
	Function cho option 3
	Tìm thông tin nhiều sinh viên theo file chứa mssv
	Xuất thông tin của sinh viên -> console
	:param file : str
	:return None
	"""
	start_time = time.time()

	# read file
	f = open(file, 'r', encoding = 'utf-8')
	arr_mssv_raw = f.read().split('\n')
	arr_mssv = []

	# check mssv hợp lệ
	for mssv in arr_mssv_raw:
		if check_mssv(mssv) == True or check_mssv(mssv) == True:	# check 2 lần -> giảm tỉ lệ sai
			arr_mssv.append(mssv)
			print(green_clr + mssv + reset_clr)
		else:
			print(red_clr + mssv + reset_clr)
	
	s = requests.Session()

	number = 1

	print()
	print(green_clr + "Đã tìm thấy", len(arr_mssv), "mssv hợp lệ." + reset_clr)

	if len(arr_mssv_raw) != len(arr_mssv):	# có mssv không hợp lệ
		print(red_clr + "Đã tìm thấy", len(arr_mssv_raw) - len(arr_mssv), "mssv không hợp lệ." + reset_clr)

	print()
	print(blue_clr + "Bắt đầu quét thông tin sinh viên..." + reset_clr)
	# Cà thông tin
	arr_thongtin = []
	for mssv in arr_mssv:
		data_post = {
			"__EVENTTARGET" : "",
			"__EVENTARGUMENT" : "", 
			"__VIEWSTATE" : "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",
			"__VIEWSTATEGENERATOR" : "CA0B0334",
			"ctl00$ContentPlaceHolder1$ctl00$txtMaSV" : mssv,
			"ctl00$ContentPlaceHolder1$ctl00$btnOK" : "OK"
		}
		x = s.post("http://thongtindaotao.sgu.edu.vn/default.aspx?page=nhapmasv&flag=XemHocPhi", data = data_post, timeout = 20)
		res = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
		soup = BeautifulSoup(res.text, 'html.parser')
		hoten = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblTenSinhVien'}).text
		gioitinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblPhai'}).text
		noisinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblNoiSinh'}).text
		lop = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblLop'}).text
		nganh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lbNganh'}).text
		khoa = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblKhoa'}).text
		hedaotao = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblHeDaoTao'}).text
		khoahoc = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblKhoaHoc'}).text
		covanhoctap = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblCVHT'}).text
		
		# ngày sinh
		r = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=thoikhoabieu&sta=1&id=' + mssv)
		soup = BeautifulSoup(r.text, 'html.parser')
		ngaysinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_lblContentTenSV'}).text.split(':')[1]

		# số điện thoại (better)
		sdt = "" #td_ls[305].text
		email = "" #td_ls[258].text

		res_2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/TKBReportView.aspx')
		soup = BeautifulSoup(res_2.text, 'html.parser')
		have_page = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})
		if len(have_page) > 0: # get đc từ in TKB
			check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
			res_3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str)
			soup = BeautifulSoup(res_3.text, 'html.parser')
			td_ls = soup.findAll('td')

			for i in range(len(td_ls)):
				if td_ls[i].text == 'Äiá»n Thoáº¡i':
					sdt = td_ls[i+1].text
				if td_ls[i].text == 'Email :':
					email = td_ls[i+1].text

		else:	# ko có in TKB do sv bảo lưu hoặc rút hồ sơ
			r1 = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
			r2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/Report_XemHocPhi.aspx', timeout = 20)
			soup = BeautifulSoup(r2.text, 'html.parser')
			check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
			r3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str, timeout = 20)
			soup = BeautifulSoup(r3.text, 'html.parser')
			#sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
			sdt = ""
			#test
			td_ls = soup.findAll('td')
			if len(td_ls) > 1275:
				sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
			else:
				for e in td_ls:
					if e.text.split(':')[0] == "Điện thoại":
						sdt = e.text.split(':')[1][1:]

		thongtin = {
			"Mã Số" : mssv,
			"Họ Tên" : hoten,
			"Giới tính" : gioitinh,
			"Ngày sinh" : ngaysinh,
			"Nơi sinh" : noisinh,
			"Lớp" : lop,
			"Ngành" : nganh,
			"Khoa" : khoa,
			"Hệ đào tạo" : hedaotao,
			"Khóa học" : khoahoc,
			"Cố vấn học tập" : covanhoctap,
			"Số điện thoại" : sdt,
			"Email" : email
		}
		
		# làm mới session sau cứ 100 lượt
		#if number%100 == 0:
		#	s = requests.Session()

		# print thong tin
		print()
		print("===" + orage_clr, number, reset_clr + "======================")
		print(blue_clr + "Mã Số:" + reset_clr, mssv)
		print(blue_clr + "Họ Tên:" + reset_clr, hoten)
		print(blue_clr + "Giới tính:" + reset_clr, gioitinh)
		print(blue_clr + "Ngày sinh:" + reset_clr, ngaysinh)
		print(blue_clr + "Nơi sinh:" + reset_clr, noisinh)
		print(blue_clr + "Lớp:" + reset_clr, lop)
		print(blue_clr + "Ngành:" + reset_clr, nganh)
		print(blue_clr + "Khoa:" + reset_clr, khoa)
		print(blue_clr + "Hệ đào tạo:" + reset_clr, hedaotao)
		print(blue_clr + "Khóa học:" + reset_clr, khoahoc)
		print(blue_clr + "Cố vấn học tập:" + reset_clr, covanhoctap)
		print(blue_clr + "Số điện thoại:" + reset_clr, sdt)
		print(blue_clr + "Email:" + reset_clr, email)
		print("========================================")
		print()
		number = number + 1

		arr_thongtin.append(thongtin)

	print()
	print((lightgreen_clr + "Time: %.3f s" + reset_clr)%(time.time() - start_time))
	print()
	print(green_clr + "Hoàn tất quét thông tin!" + reset_clr)

	# Save file
	save_choice = input(orage_clr + "Bạn có muốn lưu thông tin đã quét?" + green_clr + " [Y] -> Yes" + " | Others -> No: " + reset_clr)

	if save_choice == "Y" or save_choice == "y":
		file_choice = input(orage_clr + "Bạn muốn lưu file nào? [1] -> json | [2] -> csv | [3] -> [Both] | [Other] -> [None]: " + reset_clr)

		if file_choice == '1' or file_choice == '3':
			# save to json file
			try:
				with open('datasgu.json', 'w') as out_json_file:
					json.dump(arr_thongtin, out_json_file)
				
				print(green_clr + "Đã lưu thông tin thành công" + reset_clr)
				print(green_clr + "Thông tin được lưu ở ./datasgu.json" + reset_clr)
				#print(green_clr + "Bạn có thể vào trang " + blue_clr + "https://json-csv.com/" + green_clr + " để convert sang file excel" + reset_clr)
			except IOError:
				print(red_clr + "[I/O error] Lưu json file thất bại" + reset_clr)

		if file_choice == '2' or file_choice == '3':
			# save to csv file
			import csv
			csv_columns = ["Mã Số", "Họ Tên", "Giới tính", "Ngày sinh", "Nơi sinh", "Lớp", "Ngành", "Khoa", "Hệ đào tạo", "Khóa học", "Cố vấn học tập", "Số điện thoại", "Email"]
			
			try:
				with open("datasgu.csv", 'w', encoding = 'utf-8-sig', newline='') as out_csv_file:
					writer = csv.DictWriter(out_csv_file, fieldnames=csv_columns)
					writer.writeheader()
					for data in arr_thongtin:
						writer.writerow(data)

				print(green_clr + "Đã lưu thông tin thành công" + reset_clr)
				print(green_clr + "Thông tin được lưu ở ./datasgu.csv" + reset_clr)

			except IOError:
				print(red_clr + "[I/O error] Lưu csv file thất bại" + reset_clr)
		
	print()

def caodanhsachmssv(arr_mssv, arr_thongtin, num_size):
	s = requests.Session()

	for mssv in arr_mssv:
		data_post = {
			"__EVENTTARGET" : "",
			"__EVENTARGUMENT" : "", 
			"__VIEWSTATE" : "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",
			"__VIEWSTATEGENERATOR" : "CA0B0334",
			"ctl00$ContentPlaceHolder1$ctl00$txtMaSV" : mssv,
			"ctl00$ContentPlaceHolder1$ctl00$btnOK" : "OK"
		}
		x = s.post("http://thongtindaotao.sgu.edu.vn/default.aspx?page=nhapmasv&flag=XemHocPhi", data = data_post, timeout = 20)
		res = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
		soup = BeautifulSoup(res.text, 'html.parser')
		hoten = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblTenSinhVien'}).text
		gioitinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblPhai'}).text
		noisinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblNoiSinh'}).text
		lop = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblLop'}).text
		nganh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lbNganh'}).text
		khoa = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblKhoa'}).text
		hedaotao = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblHeDaoTao'}).text
		khoahoc = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblKhoaHoc'}).text
		covanhoctap = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ucThongTinSV_lblCVHT'}).text
		
		# ngày sinh
		r = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=thoikhoabieu&sta=1&id=' + mssv)
		soup = BeautifulSoup(r.text, 'html.parser')
		ngaysinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_lblContentTenSV'}).text.split(':')[1]

		# số điện thoại (better)
		sdt = "" #td_ls[305].text
		email = "" #td_ls[258].text

		res_2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/TKBReportView.aspx')
		soup = BeautifulSoup(res_2.text, 'html.parser')
		have_page = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})
		if len(have_page) > 0: # get đc từ in TKB
			check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
			res_3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str)
			soup = BeautifulSoup(res_3.text, 'html.parser')
			td_ls = soup.findAll('td')

			for i in range(len(td_ls)):
				if td_ls[i].text == 'Äiá»n Thoáº¡i':
					sdt = td_ls[i+1].text
				if td_ls[i].text == 'Email :':
					email = td_ls[i+1].text

		else:	# ko có in TKB do sv bảo lưu hoặc rút hồ sơ
			r1 = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
			r2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/Report_XemHocPhi.aspx', timeout = 20)
			soup = BeautifulSoup(r2.text, 'html.parser')
			check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
			r3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str, timeout = 20)
			soup = BeautifulSoup(r3.text, 'html.parser')
			#sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
			sdt = ""
			#test
			td_ls = soup.findAll('td')
			if len(td_ls) > 1275:
				sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
			else:
				for e in td_ls:
					if e.text.split(':')[0] == "Điện thoại":
						sdt = e.text.split(':')[1][1:]

		thongtin = {
			"Mã Số" : mssv,
			"Họ Tên" : hoten,
			"Giới tính" : gioitinh,
			"Ngày sinh" : ngaysinh,
			"Nơi sinh" : noisinh,
			"Lớp" : lop,
			"Ngành" : nganh,
			"Khoa" : khoa,
			"Hệ đào tạo" : hedaotao,
			"Khóa học" : khoahoc,
			"Cố vấn học tập" : covanhoctap,
			"Số điện thoại" : sdt,
			"Email" : email
		}
		
		# làm mới session sau cứ 100 lượt
		#if number%100 == 0:
		#	s = requests.Session()

		# print thong tin

		arr_thongtin.append(thongtin)
		print(green_clr, len(arr_thongtin), '/', num_size, reset_clr)

def caothongtin_file_fastscan(file):
	"""
	Function cho option 4
	Chế độ Fast Scan (dùng Phân Luồng)
	Tìm thông tin nhiều sinh viên theo file chứa mssv
	Xuất thông tin của sinh viên -> console
	:param file : str
	:return None
	"""
	start_time = time.time()

	# read file
	f = open(file, 'r', encoding = 'utf-8')
	arr_mssv_raw = f.read().split('\n')
	arr_mssv = []

	# check mssv hợp lệ
	for mssv in arr_mssv_raw:
		if check_mssv(mssv) == True or check_mssv(mssv) == True:	# check 2 lần -> giảm tỉ lệ sai
			arr_mssv.append(mssv)
			print(green_clr + mssv + reset_clr)
		else:
			print(red_clr + mssv + reset_clr)
	
	s = requests.Session()

	number = 1

	print()
	print(green_clr + "Đã tìm thấy", len(arr_mssv), "mssv hợp lệ." + reset_clr)

	if len(arr_mssv_raw) != len(arr_mssv):	# có mssv không hợp lệ
		print(red_clr + "Đã tìm thấy", len(arr_mssv_raw) - len(arr_mssv), "mssv không hợp lệ." + reset_clr)

	print()
	print(blue_clr + "Bắt đầu quét thông tin sinh viên..." + reset_clr)
	# Cà thông tin
	arr_thongtin = []
	
	thread_num = 40
	thread_ls = [None]*thread_num
	for i in range(thread_num):
		thread_ls[i] = threading.Thread(target=caodanhsachmssv, args=(arr_mssv[i*len(arr_mssv)//thread_num:(i+1)*len(arr_mssv)//thread_num], arr_thongtin, len(arr_mssv)))

	
	for i in range(thread_num):
		thread_ls[i].start()

	
	for i in range(thread_num):
		thread_ls[i].join()

	arr_thongtin.sort(key = lambda x : x["Mã Số"])

	print()
	print((lightgreen_clr + "Time: %.3f s" + reset_clr)%(time.time() - start_time))
	print()
	print(green_clr + "Hoàn tất quét thông tin!" + reset_clr)

	# Save file
	save_choice = input(orage_clr + "Bạn có muốn lưu thông tin đã quét?" + green_clr + " [Y] -> Yes" + " | Others -> No: " + reset_clr)

	if save_choice == "Y" or save_choice == "y":
		file_choice = input(orage_clr + "Bạn muốn lưu file nào? [1] -> json | [2] -> csv | [3] -> [Both] | [Other] -> [None]: " + reset_clr)

		if file_choice == '1' or file_choice == '3':
			# save to json file
			try:
				with open('datasgu.json', 'w') as out_json_file:
					json.dump(arr_thongtin, out_json_file)
				
				print(green_clr + "Đã lưu thông tin thành công" + reset_clr)
				print(green_clr + "Thông tin được lưu ở ./datasgu.json" + reset_clr)
				#print(green_clr + "Bạn có thể vào trang " + blue_clr + "https://json-csv.com/" + green_clr + " để convert sang file excel" + reset_clr)
			except IOError:
				print(red_clr + "[I/O error] Lưu json file thất bại" + reset_clr)

		if file_choice == '2' or file_choice == '3':
			# save to csv file
			import csv
			csv_columns = ["Mã Số", "Họ Tên", "Giới tính", "Ngày sinh", "Nơi sinh", "Lớp", "Ngành", "Khoa", "Hệ đào tạo", "Khóa học", "Cố vấn học tập", "Số điện thoại", "Email"]
			
			try:
				with open("datasgu.csv", 'w', encoding = 'utf-8-sig', newline='') as out_csv_file:
					writer = csv.DictWriter(out_csv_file, fieldnames=csv_columns)
					writer.writeheader()
					for data in arr_thongtin:
						writer.writerow(data)

				print(green_clr + "Đã lưu thông tin thành công" + reset_clr)
				print(green_clr + "Thông tin được lưu ở ./datasgu.csv" + reset_clr)

			except IOError:
				print(red_clr + "[I/O error] Lưu csv file thất bại" + reset_clr)
		
	print()


if __name__ == '__main__': 
	print_banner()
	print_menu()
	option = -1
	while option != '0':
		option = input(lightblue_clr + "Option: " + reset_clr)
		if option == '1':
			mssv = input("Nhập mssv: ")
			timthongtin(mssv)

		elif option == '2':
			print()
			print(orage_clr + "[Khuyến Cáo] Nên tìm dưới 100 mssv" + reset_clr)
			print()
			start_mssv = input("Tìm từ mssv: ")
			while check_mssv(start_mssv) == False:
				print(red_clr + "Mã số sinh viên ko tồn tại!\n" + reset_clr)
				start_mssv = input("Tìm từ mssv: ")

			end_mssv = input("Đến mssv: ")
			while check_mssv(end_mssv) == False:
				print(red_clr + "Mã số sinh viên ko tồn tại!\n" + reset_clr)
				end_mssv = input("Đến mssv: ")

			if check_mssv_option_2(start_mssv, end_mssv) == True:
				caothongtin(start_mssv, end_mssv)

		elif option == '3':
			print()
			print(orage_clr + "[Khuyến Cáo] Phân cách giữa các mssv là <endline>" + reset_clr)
			print()
			file = input("Nhập đường dẫn file: ")
			
			# check file exists
			from os import path
			while path.isfile(file) != True:
				print(red_clr + "File " + file + " không tồn tại" + reset_clr)
				file = input("Nhập lại đường dẫn file: ")

			caothongtin_file(file)

		elif option == '4':
			print()
			print(orage_clr + "[Khuyến Cáo] Phân cách giữa các mssv là <endline>" + reset_clr)
			print()
			file = input("Nhập đường dẫn file: ")
			
			# check file exists
			from os import path
			while path.isfile(file) != True:
				print(red_clr + "File " + file + " không tồn tại" + reset_clr)
				file = input("Nhập lại đường dẫn file: ")

			caothongtin_file_fastscan(file)

		elif option == '0':
			print()
			print(blue_clr + "Cảm ơn bạn đã sử dụng chương trình" + reset_clr)
			print(red_clr + "\nThoát\n" + reset_clr)

		else:
			print(red_clr + "\nNhập Sai\n" + reset_clr)