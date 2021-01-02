""" 
    Phần mềm tìm kiếm thông tin sinh viên SGU

    Author
    ------
    Lưu Thành Đạt
        https://github.com/Merevoli-DatLuu/SGUInfo

    Version
    -------
    v1.1 - Code Refactoring - 02/01/2021

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

from sguinfo import sguinfo

if __name__ == "__main__":
    app = sguinfo()
    app.run()
