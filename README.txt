這是一個簡單的HTTP Server，主要是練習socket programming，沒有實作HTTPS加密。

以下關於這次的project測試，有幾件事要注意：
1. 麻煩在測試的時候，一定要用google chrome瀏覽器開啟，safari會沒辦法好好地進行POST。
2. 在本機執行時，IP設為127.0.0.1，port為12724。如果要在工作站上面測試，就將197行的host值調整為工作站的IP。
3. 執行方式：$python httpserver.py #我自己的python是python3，所以如果不行就改成$python3 httpserver.py
   另外如果要丟到背景去跑的話，在後面多加上&即可：$python httpserver.py &
4. 本次完成的task有(1)留言板 (2)註冊、登入、登出功能 (3)聲音串流 (4)影片串流

