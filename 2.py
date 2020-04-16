ibm_db.active             # 检查指定的IBM_DBConnection是否处于活动状态。
ibm_db.autocommit         # 返回并设置指定的IBM_DBConnection的AUTOCOMMIT行为。
ibm_db.callproc           # 用给定名称调用存储过程
ibm_db.client_info        # 返回带有有关数据库客户端信息的只读对象。
ibm_db.close              # 关闭DB2客户机连接，并将相应的资源返回到数据库服务器。
ibm_db.column_privileges  # 返回列出表的列和相关特权的结果集。
ibm_db.columns            # 返回列出表的列和相关元数据的结果集。
ibm_db.commit             # 在指定的IBM_DBConnection上提交正在进行的事务，然后开始新的事务。
ibm_db.conn_error         # 如果未传递任何参数，则返回表示上一次数据库连接尝试失败的原因的SQLSTATE。
ibm_db.conn_errormsg      # 如果未传递任何参数，则返回一个字符串，其中包含SQLCODE和错误消息，该消息表示上次数据库连接尝试失败的原因。
ibm_db.connect            # 创建与IBM DB2通用数据库，IBM Cloudscape或Apache Derby数据库的新连接。
ibm_db.createdb           # 通过使用指定的数据库名称，代码集和模式来创建数据库
ibm_db.createdbNX         # 如果使用指定的数据库名称，代码集和模式不存在，则创建数据库。
ibm_db.cursor_type        # 返回IBM_DBStatement使用的游标类型。使用它来确定您使用的是前向游标还是可滚动游标。
ibm_db.dropdb             # 删除指定的数据库
ibm_db.exec_immediate     # 准备并执行一条SQL语句。
ibm_db.execute            # ibm_db.execute()执行由ibm_db.prepare()准备的SQL语句。如果该SQL语句返回一个结果集（例如，一个返回一个或多个结果集的SELECT语句），则可以使用ibm_db.fetch_assoc()，ibm_db.fetch_both()从stmt资源中检索一行作为元组/字典。或ibm_db.fetch_tuple()。或者，您可以使用ibm_db.fetch_row()将结果集指针移至下一行，并使用ibm_db.result()一次从该行中获取一列。有关使用ibm_db.prepare()和ibm_db.execute()而不是ibm_db.exec_immediate()的优点的简要讨论，请参考ibm_db.prepare()。要执行存储过程，请参考ibm_db.callproc()
ibm_db.execute_many       # 针对在序列seq_of_parameters中找到的所有参数序列或映射执行ibm_db.prepare()准备的SQL语句。使用此功能进行批量插入/更新/删除操作。它使用DB2 CLI的ArrayInputChaining功能来确保最少往返服务器。
ibm_db.fetch_tuple        # 返回一个由列位置索引的元组，表示结果集中的一行。
ibm_db.fetch_assoc        # 返回以列名索引的字典，表示结果集中的一行。
ibm_db.fetch_both         # 返回一个由列名和位置索引的字典，表示结果集中的一行。
ibm_db.fetch_row          # 将结果集指针设置为下一行或请求的行。
ibm_db.field_display_size # 返回在结果集中显示一列所需的最大字节数。
ibm_db.field_name         # 返回结果集中指定列的名称。
ibm_db.field_num          # 返回命名列在结果集中的位置。
ibm_db.field_precision    # 返回结果集中指定列的精度。
ibm_db.field_scale        # 返回结果集中指定列的比例。
ibm_db.field_type         # 返回结果集中指定列的数据类型。
ibm_db.field_width        # 返回结果集中指定列的当前值的宽度。对于固定长度的数据类型，这是列的最大宽度；对于可变长度的数据类型，这是列的实际宽度。
ibm_db.foreign_keys       # 返回列出表的外键的结果集。
ibm_db.free_result        # 释放与结果集关联的系统和IBM_DBConnections。脚本完成后，将隐式释放这些资源，但是您可以调用ibm_db.free_result()以在脚本结束之前显式释放结果集资源。
ibm_db.free_stmt          # 不推荐使用此API。应用程序应改用ibm_db.free_result。释放与语句资源关联的系统和IBM_DBConnections。当脚本完成时，将隐式释放这些资源，但是您可以调用ibm_db.free_stmt()来在脚本结束之前显式释放语句资源。
ibm_db.get_option         # 返回一个值，该值是连接或语句属性的当前设置。
ibm_db.next_result        # 从存储过程中请求下一个结果集。存储过程可以返回零个或多个结果集。当您以与处理简单的SELECT语句返回的结果完全相同的方式处理第一个结果集时，要从存储过程中获取第二个及后续结果集，必须调用ibm_db.next_result()函数并返回结果到一个唯一命名的Python变量。
ibm_db.num_fields         # 返回结果集中包含的字段数。这对于处理动态生成的查询返回的结果集或存储过程返回的结果集非常有用，在这种情况下，应用程序无法以其他方式知道如何检索和使用结果。
ibm_db.num_rows           # 返回由SQL语句删除，插入或更新的行数。
ibm_db.pconnect           # 返回与IBM DB2通用数据库，IBM Cloudscape，Apache Derby或Informix的持久连接。在持久连接上调用ibm_db.close时，它们不会关闭。而是将它们返回到进程范围的连接池。下次调用ibm_db.pconnect时，将在连接池中搜索匹配的连接。如果找到一个，则将其返回到应用程序，而不尝试进行新的连接。
ibm_db.prepare            # 创建一个准备好的SQL语句，该语句可以包含0个或多个参数标记（？字符），这些参数标记表示输入，输出或输入/输出的参数。您可以使用ibm_db.bind_param()或仅将输入值作为传递给ibm_db.execute()的元组，将参数传递给准备好的语句。
ibm_db.primary_keys       # 返回列出表主键的结果集。
ibm_db.procedure_columns  # 返回结果集，列出一个或多个存储过程的参数
ibm_db.procedures         # 资源ibm_db.procedures（IBM_DBConnection连接，字符串限定符，字符串模式，字符串过程）返回列出数据库中注册的存储过程的结果集。
ibm_db.recreatedb         # 删除，然后使用指定的数据库名称，代码集和模式重新创建数据库
ibm_db.result             # 从结果集中的一行返回单个列。使用ibm_db.result()返回结果集中当前**行中指定列的值。您必须先调用ibm_db.fetch_row()才能调用ibm_db.result()来设置结果集指针的位置。
ibm_db.rollback           # bool ibm_db.rollback（IBM_DBConnection连接）回滚指定IBM_DBConnection上的正在进行的事务，并开始新的事务。Python应用程序通常默认为AUTOCOMMIT模式，因此ibm_db.rollback()通常不起作用，除非已为IBM_DBConnection关闭了AUTOCOMMIT。注：如果指定的IBM_DBConnection是持久连接，则将回滚使用该持久连接的所有应用程序正在进行的所有事务。因此，不建议在需要事务的应用程序中使用持久连接。
ibm_db.server_info        # 返回一个只读对象，其中包含有关IBM DB2或Informix服务器的信息。
ibm_db.set_option         # 设置IBM_DBConnection或IBM_DBStatement的选项。您不能为结果集资源设置选项。
ibm_db.special_columns    # 返回列出表的唯一行标识符列的结果集。
ibm_db.statistics         # 返回列出表的索引和统计信息的结果集。
ibm_db.stmt_error         # 当未传递任何参数时，返回表示通过ibm_db.prepare()，ibm_db.exec_immediate()或ibm_db.callproc()返回IBM_DBStatement的最后一次尝试失败的原因的SQLSTATE。传递有效的IBM_DBStatement后，返回表示使用资源的最后一次操作失败的原因的SQLSTATE。
ibm_db.stmt_errormsg      # 如果未传递任何参数，那么将返回一个包含SQLCODE和错误消息的字符串，该字符串表示最后一次尝试通过ibm_db.prepare()，ibm_db.exec_immediate()或ibm_db.callproc()返回IBM_DBStatement的原因。传递有效的IBM_DBStatement后，将返回一个字符串，其中包含SQLCODE和错误消息，该消息表示上一次使用资源的操作失败的原因。
ibm_db.table_privileges   # 返回列出数据库中的表和相关特权的结果集。
ibm_db.tables             # 返回列出数据库中的表和相关元数据的结果集







conn_str='database=testpas4;hostname=192.168.0.182;port=50000;protocol=tcpip;uid=pas;pwd=pas'
ibm_db_conn = ibm_db.connect(conn_str,'','')

# Connect using ibm_db_dbi
import ibm_db_dbi
conn = ibm_db_dbi.Connection(ibm_db_conn)
# Execute tables API
conn.tables('DB2ADMIN', '%')
[{'TABLE_CAT': None, 'TABLE_SCHEM': 'DB2ADMIN', 'TABLE_NAME': 'MYTABLE', 'TABLE_TYPE': 'TABLE', 'REMARKS': None}]

# create table using ibm_db
create="create table mytable(id int, name varchar(50))"
ibm_db.exec_immediate(ibm_db_conn, create)
<ibm_db.IBM_DBStatement object at 0x7fcc5f44f650>

# Insert 3 rows into the table
insert = "insert into mytable values(?,?)"
params=((1,'Sanders'),(2,'Pernal'),(3,'OBrien'))
stmt_insert = ibm_db.prepare(ibm_db_conn, insert)
ibm_db.execute_many(stmt_insert,params)
3
# Fetch data using ibm_db_dbi
select="select id, name from mytable"
cur = conn.cursor()
cur.execute(select)
True
row=cur.fetchall()
print("{} \t {} \t {}".format(row[0],row[1],row[2]),end="\n")
(1, 'Sanders')   (2, 'Pernal')   (3, 'OBrien')
row=cur.fetchall()
print(row)
[]

# Fetch data using ibm_db
stmt_select = ibm_db.exec_immediate(ibm_db_conn, select)
cols = ibm_db.fetch_tuple( stmt_select )
print("%s, %s" % (cols[0], cols[1]))
1, Sanders
cols = ibm_db.fetch_tuple( stmt_select )
print("%s, %s" % (cols[0], cols[1]))
2, Pernal
cols = ibm_db.fetch_tuple( stmt_select )
print("%s, %s" % (cols[0], cols[1]))
3, OBrien
cols = ibm_db.fetch_tuple( stmt_select )
print(cols)
False

# Close connections
cur.close()
True
ibm_db.close(ibm_db_conn)
True