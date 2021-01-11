import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import threading
import json
import time


class sguinfo():
    """
    Đây là Main Class cho việc crawl dữ liệu sinh viên từ thongtindaotao.sgu.edu.vn

    Author
    ------
    Lưu Thành Đạt
        https://github.com/Merevoli-DatLuu/SGUInfo

    Version
    -------
    v1.1 - Code Refactoring - 02/01/2021

    Methods
    -------
    __init__(): None
        Hàm khởi tạo cho Class (tạm thời pass)
    print_banner(): None
        Hàm xuất banner -> CLI
    print_menu(): None
        Hàm xuât menu -> CLI
    check_mssv(mssv): bool
        Hàm kiểm tra xem mssv có hợp lệ hay không
    validate_mssv(mssv): bool
        Hàm kiểm tra xem mssv có hợp lệ hay không (better)
    validate_range_mssv(start_mssv, end_mssv): bool
        Hàm kiểm tra 2 mã mssv đầu và mssv cuối có hợp lệ hay không
    find_info(mssv): dict
        Hàm tìm thông tin của 1 sinh viên theo mssv
    print_info(mssv): None
        Hàm tìm thông tin của 1 sinh viên theo mssv, xuất thông tin -> CLI
    get_range_mssv(start_mssv, end_mssv): list
        Hàm lấy danh sách mssv hợp lệ từ start_mssv đến end_mssv
    get_range_mssv_with_print(start_mssv, end_mssv): None
        Hàm lấy danh sách mssv hợp lệ từ start_mssv đến end_mssv, xuất thông tin -> CLI
    find_by_list(arr_mssv): list
        Hàm trả về danh sách thông tin sinh viên từ mảng mssv
    find_by_list_with_print(arr_mssv): None
        Hàm trả về danh sách thông tin sinh viên từ mảng mssv. Xuất -> CLI
    def change_to_eng_info(info): dict
        Chuyển key của info sang chuẩn của api.
    save_file(arr_thongtin): None
        Hàm lưu danh sách thông tin sinh viên vào file
    find_range_info(start_mssv, end_mssv): list
        Hàm tìm thông tin nhiều sinh viên từ mssv đầu đến mssv cuối
    find_range_info_with_print(start_mssv, end_mssv): None
        Hàm tìm thông tin nhiều sinh viên từ mssv đầu đến mssv cuối. Xuất -> CLI
    find_range_info_file(file): list
        Hàm tìm thông tin nhiều sinh viên theo file chứa mssv
    find_range_info_file_with_print(file): None
        Hàm tìm thông tin nhiều sinh viên theo file chứa mssv. Xuất -> CLI
    find_by_list_thread(arr_mssv, arr_thongtin, num_size): None
        Hàm targer cho thread. Thêm thông tin mới vào arr_thongtin theo num_size
    find_by_list_thread_with_print(arr_mssv, arr_thongtin, num_size): None
        Hàm targer cho thread. Thêm thông tin mới vào arr_thongtin theo num_size. Xuất -> CLI
    find_range_info_fastscan(file): list
        Hàm tìm thông tin nhiều sinh viên theo file chứa mssv. Chế độ Fast Scan (dùng Đa Luồng)
    find_range_info_fastscan_with_print(file): None
        Hàm tìm thông tin nhiều sinh viên theo file chứa mssv, Chế độ Fast Scan (dùng Đa Luồng). Xuất -> CLI
    run(): None
        Hàm chạy chương trình chính

    Issues
    ------
    [BUG]: bị timeout [TimeoutError: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond]
    [BUG]: lỗi get ngày sinh (do server trường) (tỉ lệ thấp - lâu quá không maintain nên quên là còn lỗi này hay không:)) )
    [BUG]: k17 về trước có thể không crawl được (do html structure của trường tệ quá)
    [BUG]: Validate tỉ lệ sai ~ 1/10000
    [ISSUE]: chưa change useragent và ip

    Performance
    -----------
    Trong điều kiện server trường bình thường
    1 record ~ 2s       (option 1, 2, 3)
    100 records ~ 75s   (option 4)
    """

    def __init__(self):
        pass

    def print_banner(self):
        """
        Xuất banner -> CLI
        :return: None
        """
        print(Fore.LIGHTCYAN_EX + "  ___    ___   _   _ " + Fore.YELLOW + "  ___           __       " + Fore.RESET)
        print(Fore.LIGHTCYAN_EX + " / __|  / __| | | | |" + Fore.YELLOW + " |_ _|  _ _    / _|  ___ " + Fore.RESET)
        print(Fore.LIGHTCYAN_EX + " \\__ \\ | (_ | | |_| |" + Fore.YELLOW + "  | |  | ' \\  |  _| / _ \\ " + Fore.RESET)
        print(Fore.LIGHTCYAN_EX + " |___/  \\___|  \\___/ " + Fore.YELLOW + " |___| |_||_| |_|   \\___/" + Fore.RESET)
        print()
        print(Fore.LIGHTGREEN_EX + "  Version: v1.1" + Fore.RESET)
        print(Fore.YELLOW + "  Author: Lưu Thành Đạt" + Fore.RESET)

    def print_menu(self):
        """
        Xuất menu -> CLI
        :return: None
        """
        print()
        print(" -- " + Fore.LIGHTGREEN_EX + "MENU" + Fore.RESET + " -------------------------------")
        print(" | [1] Tìm thông tin sinh viên         |")
        print(" | [2] Quét thông tin sinh viên        |")
        print(" | [3] Quét thông tin bằng file        |")
        print(" | [4] Quét thông tin bằng file (Fast) |")
        print(" |                                     |")
        print(" | [0] Thoát                           |")
        print(" ---------------------------------------")
        print()

    def check_mssv(self, mssv):
        """
        Kiểm tra xem mssv có hợp lệ hay không
        [ISSUE]: có tỉ lệ sai ~ 1/100 (do Server trường)
        :param: mssv -> str
        :return: mssv có hợp lệ hay không -> bool
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

    def validate_mssv(self, mssv):
        """
        Kiểm tra xem mssv có hợp lệ hay không
        Fix issue của check_mssv() bằng cách check 2 lần giảm tỉ lệ xuống còn 1/10000
        :param: mssv -> str
        :return: mssv có hợp lệ hay không -> bool
        """
        if self.check_mssv(mssv) is True or self.check_mssv(mssv) is True:
            return True
        else:
            return False

    def validate_range_mssv(self, start_mssv, end_mssv):
        """
        Kiểm tra 2 mã mssv đầu và mssv cuối có hợp lệ hay không
        :param: start_mssv -> str
        :param: end_mssv -> str
        :return: mssv đầu cuối có hợp lệ hay không -> bool
        """
        if self.validate_mssv(start_mssv) is True and self.validate_mssv(end_mssv) is True:
            sub_range = int(end_mssv) - int(start_mssv)
            if sub_range < 0:
                print(Fore.LIGHTRED_EX + "[Lỗi]: Mã cuối bé hơn mã đầu" + Fore.RESET)
                return False
            elif (sub_range > 100):
                print(Fore.YELLOW + "[Cảnh Báo] Khoảng quét quá lớn có thể bị TimeoutError" + Fore.RESET)
                return True
            else:
                return True
        else:
            return False

    def find_info(self, mssv):
        """
        [Function cho option 1]
        Tìm thông tin của 1 sinh viên theo mssv
        :param: mssv -> str
        :return: Thông tin sinh viên -> dict
        """
        # check 2 lần -> giảm tỉ lệ sai
        if self.validate_mssv(mssv) is True:
            start_time = time.time()
            s = requests.Session()

            # thông tin cơ bản
            data_post = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": "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",
                "__VIEWSTATEGENERATOR": "CA0B0334",
                "ctl00$ContentPlaceHolder1$ctl00$txtMaSV": mssv,
                "ctl00$ContentPlaceHolder1$ctl00$btnOK": "OK"
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

            # số điện thoại và email (better)
            sdt = ""    # td_ls[305].text
            email = ""  # td_ls[258].text

            res_2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/TKBReportView.aspx')
            soup = BeautifulSoup(res_2.text, 'html.parser')
            have_page = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})
            if len(have_page) > 0:  # get được từ in TKB
                check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
                res_3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str)
                soup = BeautifulSoup(res_3.text, 'html.parser')
                td_ls = soup.findAll('td')

                for i in range(len(td_ls)):
                    if td_ls[i].text == 'Äiá»n Thoáº¡i':
                        sdt = td_ls[i+1].text
                    if td_ls[i].text == 'Email :':
                        email = td_ls[i+1].text
            else:   # ko có in TKB do sv bảo lưu hoặc rút hồ sơ
                r1 = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
                r2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/Report_XemHocPhi.aspx', timeout = 20)
                soup = BeautifulSoup(r2.text, 'html.parser')
                check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
                r3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str, timeout = 20)
                soup = BeautifulSoup(r3.text, 'html.parser')
                sdt = ""
                td_ls = soup.findAll('td')
                if len(td_ls) > 1275:
                    sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
                else:
                    for e in td_ls:
                        if e.text.split(':')[0] == "Điện thoại":
                            sdt = e.text.split(':')[1][1:]

            thongtin = {
                "Mã Số": mssv,
                "Họ Tên": hoten,
                "Giới tính": gioitinh,
                "Ngày sinh": ngaysinh,
                "Nơi sinh": noisinh,
                "Lớp": lop,
                "Ngành": nganh,
                "Khoa": khoa,
                "Hệ đào tạo": hedaotao,
                "Khóa học": khoahoc,
                "Cố vấn học tập": covanhoctap,
                "Số điện thoại": sdt,
                "Email": email,
                "response_time": time.time() - start_time
            }

            return thongtin
        else:
            return {}

    def print_info(self, mssv):
        """
        [Function cho option 1]
        Tìm thông tin của 1 sinh viên theo mssv
        Xuất thông tin của sinh viên -> CLI
        :param: mssv -> str
        :return: None
        """
        thongtin = self.find_info(mssv)

        if thongtin != {}:
            hoten = thongtin["Họ Tên"]
            gioitinh = thongtin["Giới tính"]
            ngaysinh = thongtin["Ngày sinh"]
            noisinh = thongtin["Nơi sinh"]
            lop = thongtin["Lớp"]
            nganh = thongtin["Ngành"]
            khoa = thongtin["Khoa"]
            hedaotao = thongtin["Hệ đào tạo"]
            khoahoc = thongtin["Khóa học"]
            covanhoctap = thongtin["Cố vấn học tập"]
            sdt = thongtin["Số điện thoại"]
            email = thongtin["Email"]
            response_time = thongtin["response_time"]

            # print thong tin
            print()
            print("==============" + Fore.YELLOW + " Thông Tin " + Fore.RESET + "==============")
            print(Fore.LIGHTCYAN_EX + "Mã Số:" + Fore.RESET, mssv)
            print(Fore.LIGHTCYAN_EX + "Họ Tên:" + Fore.RESET, hoten)
            print(Fore.LIGHTCYAN_EX + "Giới tính:" + Fore.RESET, gioitinh)
            print(Fore.LIGHTCYAN_EX + "Ngày sinh:" + Fore.RESET, ngaysinh)
            print(Fore.LIGHTCYAN_EX + "Nơi sinh:" + Fore.RESET, noisinh)
            print(Fore.LIGHTCYAN_EX + "Lớp:" + Fore.RESET, lop)
            print(Fore.LIGHTCYAN_EX + "Ngành:" + Fore.RESET, nganh)
            print(Fore.LIGHTCYAN_EX + "Khoa:" + Fore.RESET, khoa)
            print(Fore.LIGHTCYAN_EX + "Hệ đào tạo:" + Fore.RESET, hedaotao)
            print(Fore.LIGHTCYAN_EX + "Khóa học:" + Fore.RESET, khoahoc)
            print(Fore.LIGHTCYAN_EX + "Cố vấn học tập:" + Fore.RESET, covanhoctap)
            print(Fore.LIGHTCYAN_EX + "Số điện thoại:" + Fore.RESET, sdt)
            print(Fore.LIGHTCYAN_EX + "Email:" + Fore.RESET, email)
            print("========================================")
            print()
            print((Fore.LIGHTGREEN_EX + "Time: %.3f s" + Fore.RESET) % response_time)
            print()
        else:
            print(Fore.LIGHTRED_EX + "Mã số sinh viên ko tồn tại!\n" + Fore.RESET)

    def get_range_mssv(self, start_mssv, end_mssv):
        """
        Lấy danh sách mssv hợp lệ từ start_mssv đến end_mssv
        :param: start_mssv -> str
        :param: end_mssv -> str
        :return: Danh sách mssv hợp lệ -> list
        """
        arr_mssv = []
        if self.validate_range_mssv(start_mssv, end_mssv) is True:
            while (int(start_mssv) <= int(end_mssv)):
                if self.validate_mssv(start_mssv) is True:
                    arr_mssv.append(start_mssv)
                start_mssv = str(int(start_mssv) + 1)
        return arr_mssv

    def get_range_mssv_with_print(self, start_mssv, end_mssv):
        """
        Lấy danh sách mssv hợp lệ từ start_mssv đến end_mssv
        Xuất mssv hợp lệ vào CLI
        :param: start_mssv -> str
        :param: end_mssv -> str
        :return: Danh sách mssv hợp lệ -> list
        """
        arr_mssv = []
        if self.validate_range_mssv(start_mssv, end_mssv) is True:
            while (int(start_mssv) <= int(end_mssv)):
                if self.validate_mssv(start_mssv) is True:
                    arr_mssv.append(start_mssv)
                    print(Fore.LIGHTGREEN_EX + start_mssv + Fore.RESET)
                start_mssv = str(int(start_mssv) + 1)
        return arr_mssv

    def find_by_list(self, arr_mssv):
        """
        Trả về danh sách thông tin sinh viên từ mảng mssv
        :param: arr_mssv -> list
        :return: danh sách sinh viên -> list
        """

        s = requests.Session()

        # Cào thông tin
        arr_thongtin = []
        for mssv in arr_mssv:
            data_post = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": "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",
                "__VIEWSTATEGENERATOR": "CA0B0334",
                "ctl00$ContentPlaceHolder1$ctl00$txtMaSV": mssv,
                "ctl00$ContentPlaceHolder1$ctl00$btnOK": "OK"
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

            # ngày sinh [ISSUE]
            r = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=thoikhoabieu&sta=1&id=' + mssv)
            soup = BeautifulSoup(r.text, 'html.parser')
            ngaysinh = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_ctl00_lblContentTenSV'}).text.split(':')

            if len(ngaysinh) > 1:
                ngaysinh = ngaysinh[1]
            else:
                ngaysinh = ""

            # số điện thoại và email (better)
            sdt = ""    # td_ls[305].text
            email = ""  # td_ls[258].text

            res_2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/TKBReportView.aspx')
            soup = BeautifulSoup(res_2.text, 'html.parser')
            have_page = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})
            if len(have_page) > 0:  # get đc từ in TKB
                check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
                res_3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str)
                soup = BeautifulSoup(res_3.text, 'html.parser')
                td_ls = soup.findAll('td')

                for i in range(len(td_ls)):
                    if td_ls[i].text == 'Äiá»n Thoáº¡i':
                        sdt = td_ls[i+1].text
                    if td_ls[i].text == 'Email :':
                        email = td_ls[i+1].text

            else:   # ko có in TKB do sv bảo lưu hoặc rút hồ sơ
                r1 = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
                r2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/Report_XemHocPhi.aspx', timeout = 20)
                soup = BeautifulSoup(r2.text, 'html.parser')
                check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
                r3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str, timeout = 20)
                soup = BeautifulSoup(r3.text, 'html.parser')
                sdt = ""
                td_ls = soup.findAll('td')
                if len(td_ls) > 1275:
                    sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
                else:
                    for e in td_ls:
                        if e.text.split(':')[0] == "Điện thoại":
                            sdt = e.text.split(':')[1][1:]

            thongtin = {
                "Mã Số": mssv,
                "Họ Tên": hoten,
                "Giới tính": gioitinh,
                "Ngày sinh": ngaysinh,
                "Nơi sinh": noisinh,
                "Lớp": lop,
                "Ngành": nganh,
                "Khoa": khoa,
                "Hệ đào tạo": hedaotao,
                "Khóa học": khoahoc,
                "Cố vấn học tập": covanhoctap,
                "Số điện thoại": sdt,
                "Email": email
            }

            arr_thongtin.append(thongtin)

        return arr_thongtin

    def find_by_list_with_print(self, arr_mssv):
        """
        Trả về danh sách thông tin sinh viên từ mảng mssv
        Xuất thông tin -> CLI
        :param: arr_mssv -> list
        :return: None
        """

        s = requests.Session()
        number = 1
        start_time = time.time()
        arr_thongtin = []
        for mssv in arr_mssv:
            data_post = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": "/wEPDwUKLTMxNjc3NTM3NQ9kFgJmD2QWBGYPZBYEAgEPFgIeB2NvbnRlbnRkZAICDxYCHgRocmVmBSkuL01lc3NhZ2VGaWxlL2Zhdmljb24tZGFpLWhvYy1zYWktZ29uLmpwZ2QCAQ9kFggCAw9kFgJmD2QWAgIBD2QWDGYPDxYCHgRUZXh0BQxDaMOgbyBi4bqhbiBkZAIBDw8WBB4JRm9yZUNvbG9yCQAz//8eBF8hU0ICBGRkAgIPDxYEHwMJADP//x8EAgRkZAIDDw8WBh8CBRhUaGF5IMSR4buVaSBt4bqtdCBraOG6qXUfAwkAM///HwQCBGRkAgQPDxYEHwMJADP//x8EAgRkZAIFDw8WBh8CBQ3EkMSDbmcgTmjhuq1wHwMJADP//x8EAgRkZAIFD2QWqgECAQ8PFgQeCENzc0NsYXNzBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgULVFJBTkcgQ0jhu6ZkZAIDDw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgUXREFOSCBN4bukQyBDSOG7qEMgTsSCTkdkZAIFDw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgUZxJDDgU5IIEdJw4EgR0nhuqJORyBE4bqgWWRkAgcPDxYEHwUFCG91dC1tZW51HwQCAmRkAgkPDxYGHwUFCG91dC1tZW51HwQCAh4HVmlzaWJsZWhkFgICAQ8PFgIfAgUVxJDEgk5HIEvDnSBNw5ROIEjhu4xDZGQCCw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCDQ8PFgQfBQUIb3V0LW1lbnUfBAICZBYCAgEPDxYCHwIFB1hFTSBUS0JkZAIPDw8WBB8FBQhvdXQtbWVudR8EAgJkZAIRDw8WBB8FBQhvdXQtbWVudR8EAgJkFgJmDw8WAh8CBQ5YRU0gTOG7ikNIIFRISWRkAhMPDxYGHwUFCG91dC1tZW51HwQCAh8GaGQWAgIBDw8WAh8CBRRYRU0gTOG7ikNIIFRISSBM4bqgSWRkAhUPDxYGHwUFCG91dC1tZW51HwQCAh8GaGQWAgIBDw8WAh8CBRFYRU0gTOG7ikNIIFRISSBHS2RkAhcPDxYGHwUFCG91dC1tZW51HwQCAh8GaGRkAhkPDxYEHwUFCG91dC1tZW51HwQCAmRkAhsPDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBDw8WAh8CBQ5YRU0gSOG7jEMgUEjDjWRkAh0PDxYEHwUFCG91dC1tZW51HwQCAmRkAh8PDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBDw8WAh8CBQtYRU0gxJBJ4buCTWRkAiEPDxYGHwUFCG91dC1tZW51HwQCAh8GaGRkAiMPDxYEHwUFCG91dC1tZW51HwQCAmRkAiUPDxYEHwUFCG91dC1tZW51HwQCAmRkAicPDxYEHwUFCG91dC1tZW51HwQCAmRkAikPDxYEHwUFCG91dC1tZW51HwQCAmRkAisPDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBDw8WAh8CBQlYRU0gQ1TEkFRkZAItDw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgULWEVNIE3DlE4gVFFkZAIvDw8WBB8FBQhvdXQtbWVudR8EAgJkZAIxDw8WBB8FBQhvdXQtbWVudR8EAgJkZAIzDw8WBh8FBQhvdXQtbWVudR8EAgIfBmhkFgICAQ8PFgIfAgUSU+G7rEEgVFQgQ8OBIE5Iw4JOZGQCNQ8PFgYfBQUIb3V0LW1lbnUfBAICHwZoZBYCAgEPDxYCHwIFDkfDk1Agw50gS0nhur5OZGQCNw8PFgYfBQUIb3V0LW1lbnUfBAICHwZoZBYCZg8PFgIfAgUQU+G7rEEgTMOdIEzhu4pDSGRkAjkPDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBDw8WAh8CBRVRVeG6ok4gTMOdIFNJTkggVknDik5kZAI7Dw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgUiS+G6vlQgUVXhuqIgU0lOSCBWScOKTiDEkMOBTkggR0nDgWRkAj0PDxYEHwUFCG91dC1tZW51HwQCAmRkAj8PDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBD2QWAmYPDxYCHwIFGcSQw4FOSCBHScOBIEdJ4bqiTkcgROG6oFlkZAJBDw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgUUxJDEgk5HIEvDnSBUSEkgTOG6oElkZAJDDw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIeC1Bvc3RCYWNrVXJsZWRkAkUPDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBDw8WAh8CBRLEkEsgQ0hVWcOKTiBOR8OATkhkZAJHDw8WBB8FBQhvdXQtbWVudR8EAgJkZAJJDw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgUWS1EgWMOJVCBU4buQVCBOR0hJ4buGUGRkAksPDxYEHwUFCG91dC1tZW51HwQCAmRkAk0PDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBDw8WAh8CBRpDw4JVIEjhu45JIFRIxq/hu5xORyBH4bq2UGRkAk8PDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBDw8WAh8CBRPEkEsgS0jDk0EgTFXhuqxOIFROZGQCUQ8PFgQfBQUIb3V0LW1lbnUfBAICZBYCAgEPDxYCHwIFDk5I4bqsUCDEkEnhu4JNZGQCUw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCVQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCVw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCWQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCWw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCXQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCXw8PFgQfBQUIb3V0LW1lbnUfBAICZBYCAgEPDxYCHwIFJlRI4buQTkcgS8OKIEdJ4bqiTkcgVknDik4gRFVZ4buGVCBLUURLZGQCYQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCYw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCZQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCZw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCaQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCaw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCbQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCbw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCcQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCcw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCdQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCdw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCeQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCew8PFgQfBQUIb3V0LW1lbnUfBAICZGQCfQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCfw8PFgQfBQUIb3V0LW1lbnUfBAICZGQCgQEPDxYEHwUFCG91dC1tZW51HwQCAmRkAoMBDw8WBB8FBQhvdXQtbWVudR8EAgJkZAKFAQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQChwEPDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBDw8WAh8CBRdIw5NBIMSQxqBOIMSQSeG7hk4gVOG7rGRkAokBDw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgUWTkdI4buIIEThuqBZIEThuqBZIELDmWRkAosBDw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgUXxJDEgk5HIEvDnSBOR0jhu4ggUEjDiVBkZAKNAQ8PFgQfBQUIb3V0LW1lbnUfBAICZBYCAgEPDxYCHwIFEsSQxIJORyBLw50gQ09JIFRISWRkAo8BDw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgUSWEVNIEzhu4pDSCBDT0kgVEhJZGQCkQEPDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBDw8WAh8CBRtLUSBOR0hJw4pOIEPhu6hVIEtIT0EgSOG7jENkZAKTAQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQClQEPDxYEHwUFCG91dC1tZW51HwQCAmQWAgIBDw8WAh8CBSTEkMSCTkcgS8OdIFhJTiBHSeG6pFkgQ0jhu6hORyBOSOG6rE5kZAKXAQ8PFgQfBQUIb3V0LW1lbnUfBAICZBYCAgEPDxYCHwIFFUPhuqhNIE5BTkcgU0lOSCBWScOKTmRkApkBDw8WBB8FBQhvdXQtbWVudR8EAgJkZAKbAQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCnQEPDxYEHwUFCG91dC1tZW51HwQCAmRkAp8BDw8WBB8FBQhvdXQtbWVudR8EAgJkFgICAQ8PFgIfAgUkQsOBTyBCSeG7glUgUEjhu6RDIFbhu6QgTMODTkggxJDhuqBPZGQCoQEPDxYEHwUFCG91dC1tZW51HwQCAmRkAqMBDw8WBB8FBQhvdXQtbWVudR8EAgJkZAKlAQ8PFgQfBQUIb3V0LW1lbnUfBAICZGQCpwEPDxYEHwUFCG91dC1tZW51HwQCAmRkAqkBDw8WBB8FBQhvdXQtbWVudR8EAgJkZAIHD2QWAgIBD2QWAmYPZBYGAgEPEA8WBB8CBQ9Ub8OgbiB0csaw4budbmcfBmhkZGRkAgMPEA8WBB8CBRlDw6EgbmjDom4gbmfGsOG7nWkgZMO5bmc6HwZoZGRkZAIFDw8WAh8CBRtOaOG6rXAgbcOjIHPhu5EgY+G6p24geGVtOiBkZAIJD2QWCAIBDw8WAh8CBWFDb3B5cmlnaHQgwqkyMDA5IMSQ4bqhaSBo4buNYyBjaMOtbmggcXV5LiBRdeG6o24gbMO9IGLhu59pIOG7pnkgYmFuIG5ow6JuIGTDom4gVFAuIEjhu5MgQ2jDrSBNaW5oZGQCAw8PFgIfAgULVHJhbmcgQ2jhu6dkZAIFDw8WAh8CBS1UaGnhur90IGvhur8gYuG7n2kgY3R5IFBo4bqnbiBt4buBbSBBbmggUXXDom5kZAIHDw8WAh8CBQzEkOG6p3UgVHJhbmdkZGSToeMa2nNxXaNKSZPdd6SDVlTAdQ==",
                "__VIEWSTATEGENERATOR": "CA0B0334",
                "ctl00$ContentPlaceHolder1$ctl00$txtMaSV": mssv,
                "ctl00$ContentPlaceHolder1$ctl00$btnOK": "OK"
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

            # số điện thoại và email (better)
            sdt = ""    # td_ls[305].text
            email = ""  # td_ls[258].text

            res_2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/TKBReportView.aspx')
            soup = BeautifulSoup(res_2.text, 'html.parser')
            have_page = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})
            if len(have_page) > 0:  # get đc từ in TKB
                check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
                res_3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str)
                soup = BeautifulSoup(res_3.text, 'html.parser')
                td_ls = soup.findAll('td')

                for i in range(len(td_ls)):
                    if td_ls[i].text == 'Äiá»n Thoáº¡i':
                        sdt = td_ls[i+1].text
                    if td_ls[i].text == 'Email :':
                        email = td_ls[i+1].text

            else:   # ko có in TKB do sv bảo lưu hoặc rút hồ sơ
                r1 = s.get('http://thongtindaotao.sgu.edu.vn/Default.aspx?page=xemhocphi&id=' + mssv)
                r2 = s.get('http://thongtindaotao.sgu.edu.vn/Report/Report_XemHocPhi.aspx', timeout = 20)
                soup = BeautifulSoup(r2.text, 'html.parser')
                check_str = soup.findAll('iframe', {'id': 'webReportFrame_StiWebViewer1'})[0].attrs['src']
                r3 = s.get('http://thongtindaotao.sgu.edu.vn/' + check_str, timeout = 20)
                soup = BeautifulSoup(r3.text, 'html.parser')
                sdt = ""
                td_ls = soup.findAll('td')
                if len(td_ls) > 1275:
                    sdt = soup.findAll('td')[1274].text.split(':')[1][1:]
                else:
                    for e in td_ls:
                        if e.text.split(':')[0] == "Điện thoại":
                            sdt = e.text.split(':')[1][1:]

            thongtin = {
                "Mã Số": mssv,
                "Họ Tên": hoten,
                "Giới tính": gioitinh,
                "Ngày sinh": ngaysinh,
                "Nơi sinh": noisinh,
                "Lớp": lop,
                "Ngành": nganh,
                "Khoa": khoa,
                "Hệ đào tạo": hedaotao,
                "Khóa học": khoahoc,
                "Cố vấn học tập": covanhoctap,
                "Số điện thoại": sdt,
                "Email": email
            }

            # print thong tin
            print()
            print("===" + Fore.YELLOW, number, Fore.RESET + "======================")
            print(Fore.LIGHTCYAN_EX + "Mã Số:" + Fore.RESET, mssv)
            print(Fore.LIGHTCYAN_EX + "Họ Tên:" + Fore.RESET, hoten)
            print(Fore.LIGHTCYAN_EX + "Giới tính:" + Fore.RESET, gioitinh)
            print(Fore.LIGHTCYAN_EX + "Ngày sinh:" + Fore.RESET, ngaysinh)
            print(Fore.LIGHTCYAN_EX + "Nơi sinh:" + Fore.RESET, noisinh)
            print(Fore.LIGHTCYAN_EX + "Lớp:" + Fore.RESET, lop)
            print(Fore.LIGHTCYAN_EX + "Ngành:" + Fore.RESET, nganh)
            print(Fore.LIGHTCYAN_EX + "Khoa:" + Fore.RESET, khoa)
            print(Fore.LIGHTCYAN_EX + "Hệ đào tạo:" + Fore.RESET, hedaotao)
            print(Fore.LIGHTCYAN_EX + "Khóa học:" + Fore.RESET, khoahoc)
            print(Fore.LIGHTCYAN_EX + "Cố vấn học tập:" + Fore.RESET, covanhoctap)
            print(Fore.LIGHTCYAN_EX + "Số điện thoại:" + Fore.RESET, sdt)
            print(Fore.LIGHTCYAN_EX + "Email:" + Fore.RESET, email)
            print("========================================")
            print()
            number += 1

            arr_thongtin.append(thongtin)

        print()
        print((Fore.LIGHTGREEN_EX + "Time: %.3f s" + Fore.RESET) % (time.time() - start_time))
        print()
        print(Fore.LIGHTGREEN_EX + "Hoàn tất quét thông tin!" + Fore.RESET)

        # Save file
        self.save_file(arr_thongtin)

    def change_to_eng_info(self, info):
        """
        Chuyển key của info sang chuẩn của api
        :param: info -> dict
        :return: info sau khi đổi key -> dict
        """
        eng_info = {
            "Mã Số": "id",
            "Họ Tên": "name",
            "Giới tính": "gender",
            "Ngày sinh": "day_of_birth",
            "Nơi sinh": "place_of_birth",
            "Lớp": "class",
            "Ngành": "major",
            "Khoa": "department",
            "Hệ đào tạo": "training_system",
            "Khóa học": "cohort",
            "Cố vấn học tập": "academic_advisor",
            "Số điện thoại": "phone",
            "Email": "email"
        }

        for key, value in eng_info.items():
            info[value] = info[key]
            info.pop(key)

        response_key = "response_time"
        if response_key in info.keys():
            response_value = info[response_key]
            info.pop(response_key)
            info[response_key] = response_value

        return info

    def save_file(self, arr_thongtin):
        """
        Lưu danh sách thông tin sinh viên vào file
        :param: arr_thongtin -> list
        :return: None
        """
        save_choice = input(Fore.YELLOW + "Bạn có muốn lưu thông tin đã quét?" + Fore.LIGHTGREEN_EX + " [Y] -> Yes" + " | Others -> No: " + Fore.RESET)

        if save_choice in ("Y", "y"):
            file_choice = input(Fore.YELLOW + "Bạn muốn lưu file nào? [1] -> json | [2] -> csv | [3] -> [Both] | [Other] -> [None]: " + Fore.RESET)

            if file_choice in ('1', '3'):
                # save to json file
                try:
                    with open('datasgu.json', 'w') as out_json_file:
                        json.dump(arr_thongtin, out_json_file)

                    print(Fore.LIGHTGREEN_EX + "Đã lưu thông tin thành công" + Fore.RESET)
                    print(Fore.LIGHTGREEN_EX + "Thông tin được lưu ở ./datasgu.json" + Fore.RESET)
                    # print(green_clr + "Bạn có thể vào trang " + blue_clr + "https://json-csv.com/" + green_clr + " để convert sang file excel" + reset_clr)
                except IOError:
                    print(Fore.LIGHTRED_EX + "[I/O error] Lưu json file thất bại" + Fore.RESET)

            if file_choice in ('2', '3'):
                # save to csv file
                import csv
                csv_columns = ["Mã Số", "Họ Tên", "Giới tính", "Ngày sinh", "Nơi sinh", "Lớp", "Ngành", "Khoa", "Hệ đào tạo", "Khóa học", "Cố vấn học tập", "Số điện thoại", "Email"]

                try:
                    with open("datasgu.csv", 'w', encoding = 'utf-8-sig', newline='') as out_csv_file:
                        writer = csv.DictWriter(out_csv_file, fieldnames=csv_columns)
                        writer.writeheader()
                        for data in arr_thongtin:
                            writer.writerow(data)

                    print(Fore.LIGHTGREEN_EX + "Đã lưu thông tin thành công" + Fore.RESET)
                    print(Fore.LIGHTGREEN_EX + "Thông tin được lưu ở ./datasgu.csv" + Fore.RESET)

                except IOError:
                    print(Fore.LIGHTRED_EX + "[I/O error] Lưu csv file thất bại" + Fore.RESET)

        print()

    def find_range_info(self, start_mssv, end_mssv):
        """
        [Function cho option 2]
        Tìm thông tin nhiều sinh viên từ mssv đầu đến mssv cuối
        :param: start_mssv -> str
        :param: end_mssv -> str
        :return: Danh sách thông tin sinh viên -> list
        """

        arr_mssv = self.get_range_mssv(start_mssv, end_mssv)
        arr_thongtin = self.find_by_list(arr_mssv)

        return arr_thongtin

    def find_range_info_with_print(self, start_mssv, end_mssv):
        """
        [Function cho option 2]
        Tìm thông tin nhiều sinh viên từ mssv đầu đến mssv cuối
        Xuất ra thông tin nhiều sinh viên -> CLI
        :param: start_mssv -> str
        :param: end_mssv -> str
        :return: None
        """

        print(Fore.LIGHTCYAN_EX + "Đang Tìm những mssv hợp lệ..." + Fore.RESET)

        arr_mssv = self.get_range_mssv_with_print(start_mssv, end_mssv)

        print()
        print(Fore.LIGHTGREEN_EX + "Đã tìm thấy", len(arr_mssv), "mssv hợp lệ." + Fore.RESET)
        print()
        print(Fore.LIGHTCYAN_EX + "Bắt đầu quét thông tin sinh viên..." + Fore.RESET)

        # Cào thông tin
        self.find_by_list_with_print(arr_mssv)

    def find_range_info_file(self, file):
        """
        [Function cho option 3]
        Tìm thông tin nhiều sinh viên theo file chứa mssv
        :param: file -> str
        :return: Danh sách sinh viên tìm theo file -> list
        """
        # read file
        f = open(file, 'r', encoding = 'utf-8')
        arr_mssv_raw = f.read().split('\n')
        arr_mssv = []

        # check mssv hợp lệ
        for mssv in arr_mssv_raw:
            if self.validate_mssv(mssv) is True:
                arr_mssv.append(mssv)

        # Cào thông tin
        return self.find_by_list(arr_mssv)

    def find_range_info_file_with_print(self, file):
        """
        [Function cho option 3]
        Tìm thông tin nhiều sinh viên theo file chứa mssv
        Xuất thông tin của sinh viên -> CLI
        :param: file -> str
        :return: None
        """

        # read file
        f = open(file, 'r', encoding = 'utf-8')
        arr_mssv_raw = f.read().split('\n')
        arr_mssv = []

        # check mssv hợp lệ
        for mssv in arr_mssv_raw:
            if self.validate_mssv(mssv) is True:
                arr_mssv.append(mssv)
                print(Fore.LIGHTGREEN_EX + mssv + Fore.RESET)
            else:
                print(Fore.LIGHTRED_EX + mssv + Fore.RESET)

        print()
        print(Fore.LIGHTGREEN_EX + "Đã tìm thấy", len(arr_mssv), "mssv hợp lệ." + Fore.RESET)

        # có mssv không hợp lệ
        if len(arr_mssv_raw) != len(arr_mssv):
            print(Fore.LIGHTRED_EX + "Đã tìm thấy", len(arr_mssv_raw) - len(arr_mssv), "mssv không hợp lệ." + Fore.RESET)

        print()
        print(Fore.LIGHTCYAN_EX + "Bắt đầu quét thông tin sinh viên..." + Fore.RESET)

        # Cào thông tin
        self.find_by_list_with_print(arr_mssv)

    def find_by_list_thread(self, arr_mssv, arr_thongtin, num_size):
        """
        là targer cho thread.
        Thêm thông tin mới vào arr_thongtin theo num_size
        :param: arr_mssv -> list
        :param: arr_thongtin -> str
        :param: num_size -> int
        :return: None
        """

        arr_thongtin += self.find_by_list(arr_mssv)

    def find_by_list_thread_with_print(self, arr_mssv, arr_thongtin, num_size):
        """
        là targer cho thread.
        Thêm thông tin mới vào arr_thongtin theo num_size
        :param: arr_mssv -> list
        :param: arr_thongtin -> str
        :param: num_size -> int
        :return: None
        """

        arr_thongtin += self.find_by_list(arr_mssv)
        print(Fore.LIGHTGREEN_EX, len(arr_thongtin), '/', num_size, Fore.RESET)

    def find_range_info_fastscan(self, file):
        """
        [Function cho option 4]
        Chế độ Fast Scan (dùng Đa Luồng)
        Tìm thông tin nhiều sinh viên theo file chứa mssv
        :param: file -> str
        :return: danh sách thông tin sinh viên -> list
        """

        # read file
        f = open(file, 'r', encoding = 'utf-8')
        arr_mssv_raw = f.read().split('\n')
        arr_mssv = []

        # check mssv hợp lệ
        for mssv in arr_mssv_raw:
            if self.validate_mssv(mssv) is True:
                arr_mssv.append(mssv)

        # Cào thông tin
        arr_thongtin = []

        thread_num = 40
        thread_ls = [None]*thread_num
        for i in range(thread_num):
            thread_ls[i] = threading.Thread(target=self.find_by_list_thread, args=(arr_mssv[i*len(arr_mssv)//thread_num:(i+1)*len(arr_mssv)//thread_num], arr_thongtin, len(arr_mssv)))

        # khởi động luồng
        for i in range(thread_num):
            thread_ls[i].start()

        # Join luồng
        for i in range(thread_num):
            thread_ls[i].join()

        arr_thongtin.sort(key = lambda x: x["Mã Số"])

    def find_range_info_fastscan_with_print(self, file):
        """
        [Function cho option 4]
        Chế độ Fast Scan (dùng Đa Luồng)
        Tìm thông tin nhiều sinh viên theo file chứa mssv
        Xuất thông tin của sinh viên -> CLI
        :param: file -> str
        :return: None
        """
        start_time = time.time()

        # read file
        f = open(file, 'r', encoding = 'utf-8')
        arr_mssv_raw = f.read().split('\n')
        arr_mssv = []

        # check mssv hợp lệ
        for mssv in arr_mssv_raw:
            if self.validate_mssv(mssv) is True:
                arr_mssv.append(mssv)
                print(Fore.LIGHTGREEN_EX + mssv + Fore.RESET)
            else:
                print(Fore.LIGHTRED_EX + mssv + Fore.RESET)

        print()
        print(Fore.LIGHTGREEN_EX + "Đã tìm thấy", len(arr_mssv), "mssv hợp lệ." + Fore.RESET)

        if len(arr_mssv_raw) != len(arr_mssv):  # có mssv không hợp lệ
            print(Fore.LIGHTRED_EX + "Đã tìm thấy", len(arr_mssv_raw) - len(arr_mssv), "mssv không hợp lệ." + Fore.RESET)

        print()
        print(Fore.LIGHTCYAN_EX + "Bắt đầu quét thông tin sinh viên..." + Fore.RESET)

        # Cào thông tin
        arr_thongtin = []

        thread_num = min(40, len(arr_mssv))
        thread_ls = [None]*thread_num
        for i in range(thread_num):
            thread_ls[i] = threading.Thread(target=self.find_by_list_thread_with_print, args=(arr_mssv[i*len(arr_mssv)//thread_num:(i+1)*len(arr_mssv)//thread_num], arr_thongtin, len(arr_mssv)))

        # khởi động luồng
        for i in range(thread_num):
            thread_ls[i].start()

        # Join luồng
        for i in range(thread_num):
            thread_ls[i].join()

        arr_thongtin.sort(key = lambda x: x["Mã Số"])

        print()
        print((Fore.LIGHTGREEN_EX + "Time: %.3f s" + Fore.RESET) % (time.time() - start_time))
        print()
        print(Fore.LIGHTGREEN_EX + "Hoàn tất quét thông tin!" + Fore.RESET)

        # Save file
        self.save_file(arr_thongtin)

    def run(self):
        """
        Hàm chạy chương trình chính
        :return: None
        """
        # Print banner and menu
        self.print_banner()
        self.print_menu()

        option = -1
        while option != '0':
            option = input(Fore.LIGHTCYAN_EX + "Option: " + Fore.RESET)
            if option == '1':
                mssv = input("Nhập mssv: ").strip()
                self.print_info(mssv)

            elif option == '2':
                print()
                print(Fore.YELLOW + "[Khuyến Cáo] Nên tìm dưới 100 mssv" + Fore.RESET)
                print()
                start_mssv = input("Tìm từ mssv: ").strip()
                while self.validate_mssv(start_mssv) is False:
                    print(Fore.LIGHTRED_EX + "Mã số sinh viên ko tồn tại!\n" + Fore.RESET)
                    start_mssv = input("Tìm từ mssv: ").strip()

                end_mssv = input("Đến mssv: ").strip()
                while self.validate_mssv(end_mssv) is False:
                    print(Fore.LIGHTRED_EX + "Mã số sinh viên ko tồn tại!\n" + Fore.RESET)
                    end_mssv = input("Đến mssv: ").strip()

                if self.validate_range_mssv(start_mssv, end_mssv) is True:
                    self.find_range_info_with_print(start_mssv, end_mssv)

            elif option == '3':
                print()
                print(Fore.YELLOW + "[Khuyến Cáo] Phân cách giữa các mssv là <endline>" + Fore.RESET)
                print()
                file = input("Nhập đường dẫn file: ")

                # check file exists
                from os import path
                while path.isfile(file) is not True:
                    print(Fore.LIGHTRED_EX + "File " + file + " không tồn tại" + Fore.RESET)
                    file = input("Nhập lại đường dẫn file: ")

                self.find_range_info_file_with_print(file)

            elif option == '4':
                print()
                print(Fore.YELLOW + "[Khuyến Cáo] Phân cách giữa các mssv là <endline>" + Fore.RESET)
                print()
                file = input("Nhập đường dẫn file: ")

                # check file exists
                from os import path
                while path.isfile(file) is not True:
                    print(Fore.LIGHTRED_EX + "File " + file + " không tồn tại" + Fore.RESET)
                    file = input("Nhập lại đường dẫn file: ")

                self.find_range_info_fastscan_with_print(file)

            elif option == '0':
                print()
                print(Fore.LIGHTCYAN_EX + "Cảm ơn bạn đã sử dụng chương trình" + Fore.RESET)
                print(Fore.LIGHTRED_EX + "\nThoát\n" + Fore.RESET)

            else:
                print(Fore.LIGHTRED_EX + "\nNhập Sai\n" + Fore.RESET)
