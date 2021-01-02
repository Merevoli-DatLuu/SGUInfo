<div align="center">

# SGUInfo

Tra Cứu Thông Tin Sinh Viên SGU
<img src="/Screenshot/Banner.png">

![Version](https://img.shields.io/badge/Version-v1.1-cyan.svg?longCache=true&style=for-the-badge)
![AUTHOR](https://img.shields.io/badge/Author-Lưu%20Thành%20Đạt-orange.svg?longCache=true&style=for-the-badge)

</div>

---

<br>

**SGUInfo** là một công cụ dùng để tra cứu thông tin sinh viên SGU.

<br>

---


## Tính Năng

&nbsp;

* Tra cứu thông tin của một sinh viên theo mssv.

* Tra cứu thông tin của nhiều sinh viên theo khoảng mssv.

* Tra cứu thông tin của nhiều sinh viên theo file.

* Tra cứu thông tin nhanh (Multithreading).

## Cài Đặt

&nbsp;

* Chương trình chạy trên **python 3**.
* Cần package:
    * **requests**,
    * **bs4**
    * **colorama**
* Nếu chưa có package thì có thể tải package như sau:
```
python3 -m pip install -r requirements.txt
```

## Sử Dụng 

&nbsp;

* Chỉ cần chạy file `main.py` là xong.
```
python3 main.py
```

* Thư mục ```"SGUInfo\Test Files"``` có file để bạn thử tính năng **quét thông tin bằng file** (Lưu ý về số lượng quét khuyến cáo < 100).

## Issues

&nbsp;

* **[:warning: BUG]**: bị timeout [TimeoutError: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond]

* **[:warning: BUG]**: lỗi get ngày sinh (do server trường) (tỉ lệ thấp - lâu quá không maintain nên quên là còn lỗi này hay không:)) )

* **[:warning: BUG]**: k17 về trước có thể không crawl được (do html structure của trường tệ quá)

* **[:warning: BUG]**: Validate tỉ lệ sai ~ 1/10000

* **[:no_entry_sign: ISSUE]**: chưa change useragent và ip

## Screenshots

&nbsp;

<img width = "80%" src="/Screenshot/Screen1.png">
<img width = "80%" src="/Screenshot/Screen2.png">
<img width = "80%" src="/Screenshot/Screen3.png">
<img width = "80%" src="/Screenshot/Screen4.png">
<img width = "80%" src="/Screenshot/Screen5.png">
<img width = "80%" src="/Screenshot/Screen6.png">

## Contributing

&nbsp;

#### :tada: :tada: :tada: Mọi sự đóng góp đều được hoan nghênh!
* Nếu bạn phát hiện lỗi hoặc gặp vấn đề kĩ thuật thì có thể giúp mình bằng cách **submit issue**.
* Hoặc bạn muốn tham gia cùng phát triển thì có thể **create pull request**.
* Trước khi **create pull request**, hãy đảm bảo là bạn đã đọc hiểu sourcecode và tuân thủ [Standard Workflow](https://guides.github.com/introduction/flow/).