db = 'database=testpas4;'   # 数据库实例
hn = 'hostname=192.168.0.182;'  # 数据库服务器IP
p = 'port=50000;'   # 数据库端口
pc = 'protocol=tcpip;'
up = 'uid=pas;pwd=pas'  # 用户账号密码
conn_str= db + hn + p + pc + up
# tab_in包含所需要的表开头
tab_in = ('DJPD_','DKJX_','DXGX_','GRZM_','GSPZ_','GZHD_','GZJT_','GZTX_','JBGZ_','JKSJ_','JSFA_','JXBG_','JXDX_','JXGZ_','KHDX_','KHFA_','KHXJ_','NBZZ_','SGDR_','SGLR_','SJQY_','TDRW_','WGJF_','XTYW_','YJZB_','ACT_','CSB_','LSB_','XTB_')
tab_notend = ('_TMP', '_LAST', '_NEW', '_OLD', '_CS', '_BF')    # tab_notend包含不需要的表结尾
tab_notbegin = ('LSB_APP_',)   # tabl_notbegin包含不需要的表开头