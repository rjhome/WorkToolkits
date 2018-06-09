# WorkToolkits

## itsm 工单管理
  ```
  usage: itsm.py [-h] [-f [finish_status]] [-bt [begin_time]] [-et [end_time]]
                 [-abt [accept_time]] [-aet [accept_time]] [-id [ID]]
                 operate_type

  positional arguments:
    operate_type        s: show ; u: update ; a: add ; d: delete

  optional arguments:
    -h, --help          show this help message and exit
    -f [finish_status]  0: unfinished ; 1: finished
    -bt [begin_time]    begin_time : yyyymmdd (>=)
    -et [end_time]      end_time : yyyymmdd (<)
    -abt [accept_time]  accept_time (begin): yyyymmdd (>=) | 0 for today
    -aet [accept_time]  accept_time (end): yyyymmdd (<)
    -id [ID]            update itsm id : ID
  ```

## requires 相关模块
  ```
  sqlalchemy
  prettytable
  argparse
  re
  datetime
  ```
