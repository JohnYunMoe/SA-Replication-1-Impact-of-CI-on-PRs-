## Error Log: PR Collection

```
(.venv) PS C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\replication_scripts> python .\collect_pr.py

Collecting PRs from serverless/serverless...
  Processed 50 PRs...
  Processed 100 PRs...
  Processed 150 PRs...
  Processed 200 PRs...
  Processed 250 PRs...
  Processed 300 PRs...
  Processed 350 PRs...
  Processed 400 PRs...
  Processed 450 PRs...
  Processed 500 PRs...
  Processed 550 PRs...
Traceback (most recent call last):
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\urllib3\connectionpool.py", line 787, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\urllib3\connectionpool.py", line 534, in _make_request
    response = conn.getresponse()
               ^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\urllib3\connection.py", line 571, in getresponse
    httplib_response = super().getresponse()
                       ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python312\Lib\http\client.py", line 1428, in getresponse
    response.begin()
  File "C:\Python312\Lib\http\client.py", line 331, in begin
    version, status, reason = self._read_status()
                              ^^^^^^^^^^^^^^^^^^^
  File "C:\Python312\Lib\http\client.py", line 300, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
http.client.RemoteDisconnected: Remote end closed connection without response

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\requests\adapters.py", line 644, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\urllib3\connectionpool.py", line 841, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\urllib3\util\retry.py", line 490, in increment
    raise reraise(type(error), error, _stacktrace)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\urllib3\util\util.py", line 38, in reraise
    raise value.with_traceback(tb)
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\urllib3\connectionpool.py", line 787, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\urllib3\connectionpool.py", line 534, in _make_request
    response = conn.getresponse()
               ^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\urllib3\connection.py", line 571, in getresponse
    httplib_response = super().getresponse()
                       ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python312\Lib\http\client.py", line 1428, in getresponse
    response.begin()
  File "C:\Python312\Lib\http\client.py", line 331, in begin
    version, status, reason = self._read_status()
                              ^^^^^^^^^^^^^^^^^^^
  File "C:\Python312\Lib\http\client.py", line 300, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
urllib3.exceptions.ProtocolError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\replication_scripts\collect_pr.py", line 237, in <module>
    main()
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\replication_scripts\collect_pr.py", line 232, in main
    collect_pull_requests(api_base, headers, output_path)
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\replication_scripts\collect_pr.py", line 131, in collect_pull_requests
    detail = fetch_pr_detail(api_base, repo, number, headers)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\replication_scripts\collect_pr.py", line 58, in fetch_pr_detail
    data, _ = get_with_rate_limit(url, headers)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\replication_scripts\collect_pr.py", line 32, in get_with_rate_limit
    response = requests.get(url, headers=headers, params=params, timeout=30)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\requests\api.py", line 73, in get
    return request("get", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\requests\api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\requests\sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\requests\sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\University Materials\Senior Spring 2026\Software Analytics\Replication 1\SA-Replication-1-Impact-of-CI-on-PRs-\.venv\Lib\site-packages\requests\adapters.py", line 659, in send
    raise ConnectionError(err, request=request)
requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
```
