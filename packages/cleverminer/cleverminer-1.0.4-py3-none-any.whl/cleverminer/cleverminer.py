import sys #line:27
import time #line:28
import copy #line:29
from time import strftime #line:31
from time import gmtime #line:32
import pandas as pd #line:34
import numpy #line:35
class cleverminer :#line:37
    version_string ="1.0.4"#line:39
    def __init__ (OO000O00OO00OOO00 ,**OOO000O0OOOOOOO0O ):#line:41
        OO000O00OO00OOO00 ._print_disclaimer ()#line:42
        OO000O00OO00OOO00 .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:51
        OO000O00OO00OOO00 .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True }#line:55
        OO000O00OO00OOO00 .kwargs =None #line:56
        if len (OOO000O0OOOOOOO0O )>0 :#line:57
            OO000O00OO00OOO00 .kwargs =OOO000O0OOOOOOO0O #line:58
        OO000O00OO00OOO00 .verbosity ={}#line:59
        OO000O00OO00OOO00 .verbosity ['debug']=False #line:60
        OO000O00OO00OOO00 .verbosity ['print_rules']=False #line:61
        OO000O00OO00OOO00 .verbosity ['print_hashes']=True #line:62
        OO000O00OO00OOO00 .verbosity ['last_hash_time']=0 #line:63
        OO000O00OO00OOO00 .verbosity ['hint']=False #line:64
        if "opts"in OOO000O0OOOOOOO0O :#line:65
            OO000O00OO00OOO00 ._set_opts (OOO000O0OOOOOOO0O .get ("opts"))#line:66
        if "opts"in OOO000O0OOOOOOO0O :#line:67
            if "verbose"in OOO000O0OOOOOOO0O .get ('opts'):#line:68
                if OOO000O0OOOOOOO0O ['verbose'].upper ()=='FULL':#line:69
                    OO000O00OO00OOO00 .verbosity ['debug']=True #line:70
                    OO000O00OO00OOO00 .verbosity ['print_rules']=True #line:71
                    OO000O00OO00OOO00 .verbosity ['print_hashes']=False #line:72
                    OO000O00OO00OOO00 .verbosity ['hint']=True #line:73
                elif OOO000O0OOOOOOO0O ['verbose'].upper ()=='RULES':#line:74
                    OO000O00OO00OOO00 .verbosity ['debug']=False #line:75
                    OO000O00OO00OOO00 .verbosity ['print_rules']=True #line:76
                    OO000O00OO00OOO00 .verbosity ['print_hashes']=True #line:77
                    OO000O00OO00OOO00 .verbosity ['hint']=True #line:78
                elif OOO000O0OOOOOOO0O ['verbose'].upper ()=='HINT':#line:79
                    OO000O00OO00OOO00 .verbosity ['debug']=False #line:80
                    OO000O00OO00OOO00 .verbosity ['print_rules']=False #line:81
                    OO000O00OO00OOO00 .verbosity ['print_hashes']=True #line:82
                    OO000O00OO00OOO00 .verbosity ['last_hash_time']=0 #line:83
                    OO000O00OO00OOO00 .verbosity ['hint']=True #line:84
        OO000O00OO00OOO00 ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:85
        if not (OO000O00OO00OOO00 ._is_py310 ):#line:86
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:87
        else :#line:88
            if (OO000O00OO00OOO00 .verbosity ['debug']):#line:89
                print ("Python 3.10+ detected.")#line:90
        OO000O00OO00OOO00 ._initialized =False #line:91
        OO000O00OO00OOO00 ._init_data ()#line:92
        OO000O00OO00OOO00 ._init_task ()#line:93
        if len (OOO000O0OOOOOOO0O )>0 :#line:94
            if "df"in OOO000O0OOOOOOO0O :#line:95
                OO000O00OO00OOO00 ._prep_data (OOO000O0OOOOOOO0O .get ("df"))#line:96
            else :#line:97
                print ("Missing dataframe. Cannot initialize.")#line:98
                OO000O00OO00OOO00 ._initialized =False #line:99
                return #line:100
            O0OOO0O000O0OO0O0 =OOO000O0OOOOOOO0O .get ("proc",None )#line:101
            if not (O0OOO0O000O0OO0O0 ==None ):#line:102
                OO000O00OO00OOO00 ._calculate (**OOO000O0OOOOOOO0O )#line:103
            else :#line:105
                if OO000O00OO00OOO00 .verbosity ['debug']:#line:106
                    print ("INFO: just initialized")#line:107
        OO000O00OO00OOO00 ._initialized =True #line:108
    def _set_opts (O000O00O00OOOO00O ,O0000O00O0O0O000O ):#line:110
        if "no_optimizations"in O0000O00O0O0O000O :#line:111
            O000O00O00OOOO00O .options ['optimizations']=not (O0000O00O0O0O000O ['no_optimizations'])#line:112
            print ("No optimization will be made.")#line:113
        if "max_rules"in O0000O00O0O0O000O :#line:114
            O000O00O00OOOO00O .options ['max_rules']=O0000O00O0O0O000O ['max_rules']#line:115
        if "max_categories"in O0000O00O0O0O000O :#line:116
            O000O00O00OOOO00O .options ['max_categories']=O0000O00O0O0O000O ['max_categories']#line:117
            if O000O00O00OOOO00O .verbosity ['debug']==True :#line:118
                print (f"Maximum number of categories set to {O000O00O00OOOO00O.options['max_categories']}")#line:119
    def _init_data (O000000OO0OO0O000 ):#line:122
        O000000OO0OO0O000 .data ={}#line:124
        O000000OO0OO0O000 .data ["varname"]=[]#line:125
        O000000OO0OO0O000 .data ["catnames"]=[]#line:126
        O000000OO0OO0O000 .data ["vtypes"]=[]#line:127
        O000000OO0OO0O000 .data ["dm"]=[]#line:128
        O000000OO0OO0O000 .data ["rows_count"]=int (0 )#line:129
        O000000OO0OO0O000 .data ["data_prepared"]=0 #line:130
    def _init_task (OO00O0OOOO0OOO0OO ):#line:132
        if "opts"in OO00O0OOOO0OOO0OO .kwargs :#line:134
            OO00O0OOOO0OOO0OO ._set_opts (OO00O0OOOO0OOO0OO .kwargs .get ("opts"))#line:135
        OO00O0OOOO0OOO0OO .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:145
        OO00O0OOOO0OOO0OO .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:149
        OO00O0OOOO0OOO0OO .rulelist =[]#line:150
        OO00O0OOOO0OOO0OO .stats ['total_cnt']=0 #line:152
        OO00O0OOOO0OOO0OO .stats ['total_valid']=0 #line:153
        OO00O0OOOO0OOO0OO .stats ['control_number']=0 #line:154
        OO00O0OOOO0OOO0OO .result ={}#line:155
        OO00O0OOOO0OOO0OO ._opt_base =None #line:156
        OO00O0OOOO0OOO0OO ._opt_relbase =None #line:157
        OO00O0OOOO0OOO0OO ._opt_base1 =None #line:158
        OO00O0OOOO0OOO0OO ._opt_relbase1 =None #line:159
        OO00O0OOOO0OOO0OO ._opt_base2 =None #line:160
        OO00O0OOOO0OOO0OO ._opt_relbase2 =None #line:161
        O0O000OOO0OOOOO00 =None #line:162
        if not (OO00O0OOOO0OOO0OO .kwargs ==None ):#line:163
            O0O000OOO0OOOOO00 =OO00O0OOOO0OOO0OO .kwargs .get ("quantifiers",None )#line:164
            if not (O0O000OOO0OOOOO00 ==None ):#line:165
                for OO000OOO00O00O0O0 in O0O000OOO0OOOOO00 .keys ():#line:166
                    if OO000OOO00O00O0O0 .upper ()=='BASE':#line:167
                        OO00O0OOOO0OOO0OO ._opt_base =O0O000OOO0OOOOO00 .get (OO000OOO00O00O0O0 )#line:168
                    if OO000OOO00O00O0O0 .upper ()=='RELBASE':#line:169
                        OO00O0OOOO0OOO0OO ._opt_relbase =O0O000OOO0OOOOO00 .get (OO000OOO00O00O0O0 )#line:170
                    if (OO000OOO00O00O0O0 .upper ()=='FRSTBASE')|(OO000OOO00O00O0O0 .upper ()=='BASE1'):#line:171
                        OO00O0OOOO0OOO0OO ._opt_base1 =O0O000OOO0OOOOO00 .get (OO000OOO00O00O0O0 )#line:172
                    if (OO000OOO00O00O0O0 .upper ()=='SCNDBASE')|(OO000OOO00O00O0O0 .upper ()=='BASE2'):#line:173
                        OO00O0OOOO0OOO0OO ._opt_base2 =O0O000OOO0OOOOO00 .get (OO000OOO00O00O0O0 )#line:174
                    if (OO000OOO00O00O0O0 .upper ()=='FRSTRELBASE')|(OO000OOO00O00O0O0 .upper ()=='RELBASE1'):#line:175
                        OO00O0OOOO0OOO0OO ._opt_relbase1 =O0O000OOO0OOOOO00 .get (OO000OOO00O00O0O0 )#line:176
                    if (OO000OOO00O00O0O0 .upper ()=='SCNDRELBASE')|(OO000OOO00O00O0O0 .upper ()=='RELBASE2'):#line:177
                        OO00O0OOOO0OOO0OO ._opt_relbase2 =O0O000OOO0OOOOO00 .get (OO000OOO00O00O0O0 )#line:178
            else :#line:179
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:180
        else :#line:181
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:182
    def mine (OO000OOOO0OOOO000 ,**O0OO00O0000OOO0OO ):#line:185
        if not (OO000OOOO0OOOO000 ._initialized ):#line:186
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:187
            return #line:188
        OO000OOOO0OOOO000 .kwargs =None #line:189
        if len (O0OO00O0000OOO0OO )>0 :#line:190
            OO000OOOO0OOOO000 .kwargs =O0OO00O0000OOO0OO #line:191
        OO000OOOO0OOOO000 ._init_task ()#line:192
        if len (O0OO00O0000OOO0OO )>0 :#line:193
            O00OO00O00OOO0O0O =O0OO00O0000OOO0OO .get ("proc",None )#line:194
            if not (O00OO00O00OOO0O0O ==None ):#line:195
                OO000OOOO0OOOO000 ._calc_all (**O0OO00O0000OOO0OO )#line:196
            else :#line:197
                print ("Rule mining procedure missing")#line:198
    def _get_ver (OO0OO00OO0OO00O0O ):#line:201
        return OO0OO00OO0OO00O0O .version_string #line:202
    def _print_disclaimer (O00OO00OO00O0O000 ):#line:204
        print (f"Cleverminer version {O00OO00OO00O0O000._get_ver()}.")#line:206
    def _prep_data (O0OOO00OOOO0O0000 ,OOOO0O00OOO000000 ):#line:213
        print ("Starting data preparation ...")#line:214
        O0OOO00OOOO0O0000 ._init_data ()#line:215
        O0OOO00OOOO0O0000 .stats ['start_prep_time']=time .time ()#line:216
        O0OOO00OOOO0O0000 .data ["rows_count"]=OOOO0O00OOO000000 .shape [0 ]#line:217
        for OO00000O000OO0OO0 in OOOO0O00OOO000000 .select_dtypes (exclude =['category']).columns :#line:218
            OOOO0O00OOO000000 [OO00000O000OO0OO0 ]=OOOO0O00OOO000000 [OO00000O000OO0OO0 ].apply (str )#line:219
        try :#line:220
            O000OO0OOOO0OO0O0 =pd .DataFrame .from_records ([(OO00OO00OO0000O0O ,OOOO0O00OOO000000 [OO00OO00OO0000O0O ].nunique ())for OO00OO00OO0000O0O in OOOO0O00OOO000000 .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:222
        except :#line:223
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:224
            O00O0OO00000OOOOO =""#line:225
            try :#line:226
                for OO00000O000OO0OO0 in OOOO0O00OOO000000 .columns :#line:227
                    O00O0OO00000OOOOO =OO00000O000OO0OO0 #line:228
                    print (f"...column {OO00000O000OO0OO0} has {int(OOOO0O00OOO000000[OO00000O000OO0OO0].nunique())} values")#line:229
            except :#line:230
                print (f"... detected : column {O00O0OO00000OOOOO} has unsupported type: {type(OOOO0O00OOO000000[OO00000O000OO0OO0])}.")#line:231
                exit (1 )#line:232
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:233
            exit (1 )#line:234
        if O0OOO00OOOO0O0000 .verbosity ['hint']:#line:237
            print ("Quick profile of input data: unique value counts are:")#line:238
            print (O000OO0OOOO0OO0O0 )#line:239
            for OO00000O000OO0OO0 in OOOO0O00OOO000000 .columns :#line:240
                if OOOO0O00OOO000000 [OO00000O000OO0OO0 ].nunique ()<O0OOO00OOOO0O0000 .options ['max_categories']:#line:241
                    OOOO0O00OOO000000 [OO00000O000OO0OO0 ]=OOOO0O00OOO000000 [OO00000O000OO0OO0 ].astype ('category')#line:242
                else :#line:243
                    print (f"WARNING: attribute {OO00000O000OO0OO0} has more than {O0OOO00OOOO0O0000.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:244
                    del OOOO0O00OOO000000 [OO00000O000OO0OO0 ]#line:245
        print ("Encoding columns into bit-form...")#line:246
        O00OOOO00O0OOOOO0 =0 #line:247
        OO000O0OOO000OO0O =0 #line:248
        for OOO0O00000OOO00OO in OOOO0O00OOO000000 :#line:249
            if O0OOO00OOOO0O0000 .verbosity ['debug']:#line:251
                print ('Column: '+OOO0O00000OOO00OO )#line:252
            O0OOO00OOOO0O0000 .data ["varname"].append (OOO0O00000OOO00OO )#line:253
            O000OO0000O00O0OO =pd .get_dummies (OOOO0O00OOO000000 [OOO0O00000OOO00OO ])#line:254
            OO00O00O0000O0O00 =0 #line:255
            if (OOOO0O00OOO000000 .dtypes [OOO0O00000OOO00OO ].name =='category'):#line:256
                OO00O00O0000O0O00 =1 #line:257
            O0OOO00OOOO0O0000 .data ["vtypes"].append (OO00O00O0000O0O00 )#line:258
            O00OO00O0O0O0OOOO =0 #line:261
            OO00O000O0OO0O0OO =[]#line:262
            OO00OOO0OO0O00OOO =[]#line:263
            for O0O0OOO0OOOOO0OOO in O000OO0000O00O0OO :#line:265
                if O0OOO00OOOO0O0000 .verbosity ['debug']:#line:267
                    print ('....category : '+str (O0O0OOO0OOOOO0OOO )+" @ "+str (time .time ()))#line:268
                OO00O000O0OO0O0OO .append (O0O0OOO0OOOOO0OOO )#line:269
                O0OO0000O00OOO000 =int (0 )#line:270
                O00OOOO0O00O0O0OO =O000OO0000O00O0OO [O0O0OOO0OOOOO0OOO ].values #line:271
                O000O0OOOO0O0O0OO =numpy .packbits (O00OOOO0O00O0O0OO ,bitorder ='little')#line:273
                O0OO0000O00OOO000 =int .from_bytes (O000O0OOOO0O0O0OO ,byteorder ='little')#line:274
                OO00OOO0OO0O00OOO .append (O0OO0000O00OOO000 )#line:275
                O00OO00O0O0O0OOOO +=1 #line:293
                OO000O0OOO000OO0O +=1 #line:294
            O0OOO00OOOO0O0000 .data ["catnames"].append (OO00O000O0OO0O0OO )#line:296
            O0OOO00OOOO0O0000 .data ["dm"].append (OO00OOO0OO0O00OOO )#line:297
        print ("Encoding columns into bit-form...done")#line:299
        if O0OOO00OOOO0O0000 .verbosity ['hint']:#line:300
            print (f"List of attributes for analysis is: {O0OOO00OOOO0O0000.data['varname']}")#line:301
            print (f"List of category names for individual attributes is : {O0OOO00OOOO0O0000.data['catnames']}")#line:302
        if O0OOO00OOOO0O0000 .verbosity ['debug']:#line:303
            print (f"List of vtypes is (all should be 1) : {O0OOO00OOOO0O0000.data['vtypes']}")#line:304
        O0OOO00OOOO0O0000 .data ["data_prepared"]=1 #line:306
        print ("Data preparation finished.")#line:307
        if O0OOO00OOOO0O0000 .verbosity ['debug']:#line:308
            print ('Number of variables : '+str (len (O0OOO00OOOO0O0000 .data ["dm"])))#line:309
            print ('Total number of categories in all variables : '+str (OO000O0OOO000OO0O ))#line:310
        O0OOO00OOOO0O0000 .stats ['end_prep_time']=time .time ()#line:311
        if O0OOO00OOOO0O0000 .verbosity ['debug']:#line:312
            print ('Time needed for data preparation : ',str (O0OOO00OOOO0O0000 .stats ['end_prep_time']-O0OOO00OOOO0O0000 .stats ['start_prep_time']))#line:313
    def _bitcount (O00OO00000O000O0O ,OO0OO0OOO0OOO00O0 ):#line:315
        OOO00O000O00OOO0O =None #line:316
        if (O00OO00000O000O0O ._is_py310 ):#line:317
            OOO00O000O00OOO0O =OO0OO0OOO0OOO00O0 .bit_count ()#line:318
        else :#line:319
            OOO00O000O00OOO0O =bin (OO0OO0OOO0OOO00O0 ).count ("1")#line:320
        return OOO00O000O00OOO0O #line:321
    def _verifyCF (OOOO0000OO00O0OOO ,_O00OO000O0O0O000O ):#line:324
        OO0OO0000OO0000O0 =OOOO0000OO00O0OOO ._bitcount (_O00OO000O0O0O000O )#line:325
        O00000OOOOOO0O00O =[]#line:326
        OOOO0OO0OOOO0OO00 =[]#line:327
        O0O0OOOO00O00OOO0 =0 #line:328
        OOOO0O0O0O0O0OOO0 =0 #line:329
        O0O0OO00OOOO0O0O0 =0 #line:330
        OOO00O00O0OO0OO00 =0 #line:331
        O000OOOO0OO0O00O0 =0 #line:332
        O00O0OOOOOOOOOOO0 =0 #line:333
        OOO00O00OOO0O0OOO =0 #line:334
        O00O0OO00O0O00000 =0 #line:335
        O0OOO0O00O00000O0 =0 #line:336
        O0OOOO0O0OO0000O0 =0 #line:337
        O0OOOOOO0O00000OO =0 #line:338
        OOOOO00OO000OOOOO =[]#line:339
        if ('aad_weights'in OOOO0000OO00O0OOO .quantifiers ):#line:340
            O0OOOO0O0OO0000O0 =1 #line:341
            OOOOO0OO0OOO0000O =[]#line:342
            OOOOO00OO000OOOOO =OOOO0000OO00O0OOO .quantifiers .get ('aad_weights')#line:343
        O00OOO0OO00OOOOO0 =OOOO0000OO00O0OOO .data ["dm"][OOOO0000OO00O0OOO .data ["varname"].index (OOOO0000OO00O0OOO .kwargs .get ('target'))]#line:344
        for O0O00O0000O000000 in range (len (O00OOO0OO00OOOOO0 )):#line:345
            OOOO0O0O0O0O0OOO0 =O0O0OOOO00O00OOO0 #line:347
            O0O0OOOO00O00OOO0 =OOOO0000OO00O0OOO ._bitcount (_O00OO000O0O0O000O &O00OOO0OO00OOOOO0 [O0O00O0000O000000 ])#line:348
            O00000OOOOOO0O00O .append (O0O0OOOO00O00OOO0 )#line:349
            if O0O00O0000O000000 >0 :#line:350
                if (O0O0OOOO00O00OOO0 >OOOO0O0O0O0O0OOO0 ):#line:351
                    if (O0O0OO00OOOO0O0O0 ==1 ):#line:352
                        O00O0OO00O0O00000 +=1 #line:353
                    else :#line:354
                        O00O0OO00O0O00000 =1 #line:355
                    if O00O0OO00O0O00000 >OOO00O00O0OO0OO00 :#line:356
                        OOO00O00O0OO0OO00 =O00O0OO00O0O00000 #line:357
                    O0O0OO00OOOO0O0O0 =1 #line:358
                    O00O0OOOOOOOOOOO0 +=1 #line:359
                if (O0O0OOOO00O00OOO0 <OOOO0O0O0O0O0OOO0 ):#line:360
                    if (O0O0OO00OOOO0O0O0 ==-1 ):#line:361
                        O0OOO0O00O00000O0 +=1 #line:362
                    else :#line:363
                        O0OOO0O00O00000O0 =1 #line:364
                    if O0OOO0O00O00000O0 >O000OOOO0OO0O00O0 :#line:365
                        O000OOOO0OO0O00O0 =O0OOO0O00O00000O0 #line:366
                    O0O0OO00OOOO0O0O0 =-1 #line:367
                    OOO00O00OOO0O0OOO +=1 #line:368
                if (O0O0OOOO00O00OOO0 ==OOOO0O0O0O0O0OOO0 ):#line:369
                    O0O0OO00OOOO0O0O0 =0 #line:370
                    O0OOO0O00O00000O0 =0 #line:371
                    O00O0OO00O0O00000 =0 #line:372
            if (O0OOOO0O0OO0000O0 ):#line:374
                OO0OOO0O00OOO00O0 =OOOO0000OO00O0OOO ._bitcount (O00OOO0OO00OOOOO0 [O0O00O0000O000000 ])#line:375
                OOOOO0OO0OOO0000O .append (OO0OOO0O00OOO00O0 )#line:376
        if (O0OOOO0O0OO0000O0 &sum (O00000OOOOOO0O00O )>0 ):#line:378
            for O0O00O0000O000000 in range (len (O00OOO0OO00OOOOO0 )):#line:379
                if OOOOO0OO0OOO0000O [O0O00O0000O000000 ]>0 :#line:380
                    if O00000OOOOOO0O00O [O0O00O0000O000000 ]/sum (O00000OOOOOO0O00O )>OOOOO0OO0OOO0000O [O0O00O0000O000000 ]/sum (OOOOO0OO0OOO0000O ):#line:382
                        O0OOOOOO0O00000OO +=OOOOO00OO000OOOOO [O0O00O0000O000000 ]*((O00000OOOOOO0O00O [O0O00O0000O000000 ]/sum (O00000OOOOOO0O00O ))/(OOOOO0OO0OOO0000O [O0O00O0000O000000 ]/sum (OOOOO0OO0OOO0000O ))-1 )#line:383
        OOO0000OOOO00O0OO =True #line:386
        for O0OOO000OOOOOOOO0 in OOOO0000OO00O0OOO .quantifiers .keys ():#line:387
            if O0OOO000OOOOOOOO0 .upper ()=='BASE':#line:388
                OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=OO0OO0000OO0000O0 )#line:389
            if O0OOO000OOOOOOOO0 .upper ()=='RELBASE':#line:390
                OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=OO0OO0000OO0000O0 *1.0 /OOOO0000OO00O0OOO .data ["rows_count"])#line:391
            if O0OOO000OOOOOOOO0 .upper ()=='S_UP':#line:392
                OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=OOO00O00O0OO0OO00 )#line:393
            if O0OOO000OOOOOOOO0 .upper ()=='S_DOWN':#line:394
                OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=O000OOOO0OO0O00O0 )#line:395
            if O0OOO000OOOOOOOO0 .upper ()=='S_ANY_UP':#line:396
                OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=OOO00O00O0OO0OO00 )#line:397
            if O0OOO000OOOOOOOO0 .upper ()=='S_ANY_DOWN':#line:398
                OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=O000OOOO0OO0O00O0 )#line:399
            if O0OOO000OOOOOOOO0 .upper ()=='MAX':#line:400
                OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=max (O00000OOOOOO0O00O ))#line:401
            if O0OOO000OOOOOOOO0 .upper ()=='MIN':#line:402
                OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=min (O00000OOOOOO0O00O ))#line:403
            if O0OOO000OOOOOOOO0 .upper ()=='RELMAX':#line:404
                if sum (O00000OOOOOO0O00O )>0 :#line:405
                    OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=max (O00000OOOOOO0O00O )*1.0 /sum (O00000OOOOOO0O00O ))#line:406
                else :#line:407
                    OOO0000OOOO00O0OO =False #line:408
            if O0OOO000OOOOOOOO0 .upper ()=='RELMAX_LEQ':#line:409
                if sum (O00000OOOOOO0O00O )>0 :#line:410
                    OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )>=max (O00000OOOOOO0O00O )*1.0 /sum (O00000OOOOOO0O00O ))#line:411
                else :#line:412
                    OOO0000OOOO00O0OO =False #line:413
            if O0OOO000OOOOOOOO0 .upper ()=='RELMIN':#line:414
                if sum (O00000OOOOOO0O00O )>0 :#line:415
                    OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=min (O00000OOOOOO0O00O )*1.0 /sum (O00000OOOOOO0O00O ))#line:416
                else :#line:417
                    OOO0000OOOO00O0OO =False #line:418
            if O0OOO000OOOOOOOO0 .upper ()=='RELMIN_LEQ':#line:419
                if sum (O00000OOOOOO0O00O )>0 :#line:420
                    OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )>=min (O00000OOOOOO0O00O )*1.0 /sum (O00000OOOOOO0O00O ))#line:421
                else :#line:422
                    OOO0000OOOO00O0OO =False #line:423
            if O0OOO000OOOOOOOO0 .upper ()=='AAD':#line:424
                OOO0000OOOO00O0OO =OOO0000OOOO00O0OO and (OOOO0000OO00O0OOO .quantifiers .get (O0OOO000OOOOOOOO0 )<=O0OOOOOO0O00000OO )#line:425
        O00000OOOOO0O00O0 ={}#line:427
        if OOO0000OOOO00O0OO ==True :#line:428
            OOOO0000OO00O0OOO .stats ['total_valid']+=1 #line:430
            O00000OOOOO0O00O0 ["base"]=OO0OO0000OO0000O0 #line:431
            O00000OOOOO0O00O0 ["rel_base"]=OO0OO0000OO0000O0 *1.0 /OOOO0000OO00O0OOO .data ["rows_count"]#line:432
            O00000OOOOO0O00O0 ["s_up"]=OOO00O00O0OO0OO00 #line:433
            O00000OOOOO0O00O0 ["s_down"]=O000OOOO0OO0O00O0 #line:434
            O00000OOOOO0O00O0 ["s_any_up"]=O00O0OOOOOOOOOOO0 #line:435
            O00000OOOOO0O00O0 ["s_any_down"]=OOO00O00OOO0O0OOO #line:436
            O00000OOOOO0O00O0 ["max"]=max (O00000OOOOOO0O00O )#line:437
            O00000OOOOO0O00O0 ["min"]=min (O00000OOOOOO0O00O )#line:438
            if sum (O00000OOOOOO0O00O )>0 :#line:441
                O00000OOOOO0O00O0 ["rel_max"]=max (O00000OOOOOO0O00O )*1.0 /sum (O00000OOOOOO0O00O )#line:442
                O00000OOOOO0O00O0 ["rel_min"]=min (O00000OOOOOO0O00O )*1.0 /sum (O00000OOOOOO0O00O )#line:443
            else :#line:444
                O00000OOOOO0O00O0 ["rel_max"]=0 #line:445
                O00000OOOOO0O00O0 ["rel_min"]=0 #line:446
            O00000OOOOO0O00O0 ["hist"]=O00000OOOOOO0O00O #line:447
            if O0OOOO0O0OO0000O0 :#line:448
                O00000OOOOO0O00O0 ["aad"]=O0OOOOOO0O00000OO #line:449
                O00000OOOOO0O00O0 ["hist_full"]=OOOOO0OO0OOO0000O #line:450
                O00000OOOOO0O00O0 ["rel_hist"]=[OOOOO0O000000O00O /sum (O00000OOOOOO0O00O )for OOOOO0O000000O00O in O00000OOOOOO0O00O ]#line:451
                O00000OOOOO0O00O0 ["rel_hist_full"]=[O0OOO000000OOO0O0 /sum (OOOOO0OO0OOO0000O )for O0OOO000000OOO0O0 in OOOOO0OO0OOO0000O ]#line:452
        return OOO0000OOOO00O0OO ,O00000OOOOO0O00O0 #line:454
    def _verifyUIC (OO0O00000OOO0OO0O ,_OOOOOOO0000OOO00O ):#line:456
        OOOOO00O00OOO00O0 ={}#line:457
        O0000O000O00OO0O0 =0 #line:458
        for OOO000000O0OOO0O0 in OO0O00000OOO0OO0O .task_actinfo ['cedents']:#line:459
            OOOOO00O00OOO00O0 [OOO000000O0OOO0O0 ['cedent_type']]=OOO000000O0OOO0O0 ['filter_value']#line:461
            O0000O000O00OO0O0 =O0000O000O00OO0O0 +1 #line:462
        O0O0O0OO00OOO0O00 =OO0O00000OOO0OO0O ._bitcount (_OOOOOOO0000OOO00O )#line:464
        OOOOO00OO0O0OO000 =[]#line:465
        O00OO0000O0OOO0O0 =0 #line:466
        OOO0OOOO0O00OO0OO =0 #line:467
        O0OOOO0O0000O00O0 =0 #line:468
        OOO000OOOO0OO0OO0 =[]#line:469
        O0OOOO0OO0O000OOO =[]#line:470
        if ('aad_weights'in OO0O00000OOO0OO0O .quantifiers ):#line:471
            OOO000OOOO0OO0OO0 =OO0O00000OOO0OO0O .quantifiers .get ('aad_weights')#line:472
            OOO0OOOO0O00OO0OO =1 #line:473
        OOO00O0O0O0O000OO =OO0O00000OOO0OO0O .data ["dm"][OO0O00000OOO0OO0O .data ["varname"].index (OO0O00000OOO0OO0O .kwargs .get ('target'))]#line:474
        for O0000OO00O0O0O0OO in range (len (OOO00O0O0O0O000OO )):#line:475
            OOOO00000O0O0OOOO =O00OO0000O0OOO0O0 #line:477
            O00OO0000O0OOO0O0 =OO0O00000OOO0OO0O ._bitcount (_OOOOOOO0000OOO00O &OOO00O0O0O0O000OO [O0000OO00O0O0O0OO ])#line:478
            OOOOO00OO0O0OO000 .append (O00OO0000O0OOO0O0 )#line:479
            OO0OO0O00OOO0000O =OO0O00000OOO0OO0O ._bitcount (OOOOO00O00OOO00O0 ['cond']&OOO00O0O0O0O000OO [O0000OO00O0O0O0OO ])#line:482
            O0OOOO0OO0O000OOO .append (OO0OO0O00OOO0000O )#line:483
        if (OOO0OOOO0O00OO0OO &sum (OOOOO00OO0O0OO000 )>0 ):#line:485
            for O0000OO00O0O0O0OO in range (len (OOO00O0O0O0O000OO )):#line:486
                if O0OOOO0OO0O000OOO [O0000OO00O0O0O0OO ]>0 :#line:487
                    if OOOOO00OO0O0OO000 [O0000OO00O0O0O0OO ]/sum (OOOOO00OO0O0OO000 )>O0OOOO0OO0O000OOO [O0000OO00O0O0O0OO ]/sum (O0OOOO0OO0O000OOO ):#line:489
                        O0OOOO0O0000O00O0 +=OOO000OOOO0OO0OO0 [O0000OO00O0O0O0OO ]*((OOOOO00OO0O0OO000 [O0000OO00O0O0O0OO ]/sum (OOOOO00OO0O0OO000 ))/(O0OOOO0OO0O000OOO [O0000OO00O0O0O0OO ]/sum (O0OOOO0OO0O000OOO ))-1 )#line:490
        OO00000O000000OOO =True #line:493
        for OOOO00000OOO000OO in OO0O00000OOO0OO0O .quantifiers .keys ():#line:494
            if OOOO00000OOO000OO .upper ()=='BASE':#line:495
                OO00000O000000OOO =OO00000O000000OOO and (OO0O00000OOO0OO0O .quantifiers .get (OOOO00000OOO000OO )<=O0O0O0OO00OOO0O00 )#line:496
            if OOOO00000OOO000OO .upper ()=='RELBASE':#line:497
                OO00000O000000OOO =OO00000O000000OOO and (OO0O00000OOO0OO0O .quantifiers .get (OOOO00000OOO000OO )<=O0O0O0OO00OOO0O00 *1.0 /OO0O00000OOO0OO0O .data ["rows_count"])#line:498
            if OOOO00000OOO000OO .upper ()=='AAD_SCORE':#line:499
                OO00000O000000OOO =OO00000O000000OOO and (OO0O00000OOO0OO0O .quantifiers .get (OOOO00000OOO000OO )<=O0OOOO0O0000O00O0 )#line:500
        OO0OOOOOO0O0O0O0O ={}#line:502
        if OO00000O000000OOO ==True :#line:503
            OO0O00000OOO0OO0O .stats ['total_valid']+=1 #line:505
            OO0OOOOOO0O0O0O0O ["base"]=O0O0O0OO00OOO0O00 #line:506
            OO0OOOOOO0O0O0O0O ["rel_base"]=O0O0O0OO00OOO0O00 *1.0 /OO0O00000OOO0OO0O .data ["rows_count"]#line:507
            OO0OOOOOO0O0O0O0O ["hist"]=OOOOO00OO0O0OO000 #line:508
            OO0OOOOOO0O0O0O0O ["aad_score"]=O0OOOO0O0000O00O0 #line:510
            OO0OOOOOO0O0O0O0O ["hist_cond"]=O0OOOO0OO0O000OOO #line:511
            OO0OOOOOO0O0O0O0O ["rel_hist"]=[OOO0OOO0O0OO0000O /sum (OOOOO00OO0O0OO000 )for OOO0OOO0O0OO0000O in OOOOO00OO0O0OO000 ]#line:512
            OO0OOOOOO0O0O0O0O ["rel_hist_cond"]=[O0O0OO000O00OO0O0 /sum (O0OOOO0OO0O000OOO )for O0O0OO000O00OO0O0 in O0OOOO0OO0O000OOO ]#line:513
        return OO00000O000000OOO ,OO0OOOOOO0O0O0O0O #line:515
    def _verify4ft (OO0OO0000OO00O000 ,_O0O00OOOO0OOO00OO ):#line:517
        OO000OO0O000OOO00 ={}#line:518
        OOOOOO00O00O00O00 =0 #line:519
        for OO000OOOO0O0O00OO in OO0OO0000OO00O000 .task_actinfo ['cedents']:#line:520
            OO000OO0O000OOO00 [OO000OOOO0O0O00OO ['cedent_type']]=OO000OOOO0O0O00OO ['filter_value']#line:522
            OOOOOO00O00O00O00 =OOOOOO00O00O00O00 +1 #line:523
        OO0OO0OOO0000OOO0 =OO0OO0000OO00O000 ._bitcount (OO000OO0O000OOO00 ['ante']&OO000OO0O000OOO00 ['succ']&OO000OO0O000OOO00 ['cond'])#line:525
        OOOOO00O0O0O0000O =None #line:526
        OOOOO00O0O0O0000O =0 #line:527
        if OO0OO0OOO0000OOO0 >0 :#line:536
            OOOOO00O0O0O0000O =OO0OO0000OO00O000 ._bitcount (OO000OO0O000OOO00 ['ante']&OO000OO0O000OOO00 ['succ']&OO000OO0O000OOO00 ['cond'])*1.0 /OO0OO0000OO00O000 ._bitcount (OO000OO0O000OOO00 ['ante']&OO000OO0O000OOO00 ['cond'])#line:537
        OO00OOO0OO00OO0OO =1 <<OO0OO0000OO00O000 .data ["rows_count"]#line:539
        OOOOO0O0O000O00OO =OO0OO0000OO00O000 ._bitcount (OO000OO0O000OOO00 ['ante']&OO000OO0O000OOO00 ['succ']&OO000OO0O000OOO00 ['cond'])#line:540
        O0OOO000OOOO0OO00 =OO0OO0000OO00O000 ._bitcount (OO000OO0O000OOO00 ['ante']&~(OO00OOO0OO00OO0OO |OO000OO0O000OOO00 ['succ'])&OO000OO0O000OOO00 ['cond'])#line:541
        OO000OOOO0O0O00OO =OO0OO0000OO00O000 ._bitcount (~(OO00OOO0OO00OO0OO |OO000OO0O000OOO00 ['ante'])&OO000OO0O000OOO00 ['succ']&OO000OO0O000OOO00 ['cond'])#line:542
        O0O0O00O0O0OO000O =OO0OO0000OO00O000 ._bitcount (~(OO00OOO0OO00OO0OO |OO000OO0O000OOO00 ['ante'])&~(OO00OOO0OO00OO0OO |OO000OO0O000OOO00 ['succ'])&OO000OO0O000OOO00 ['cond'])#line:543
        O000000000OOOO000 =0 #line:544
        if (OOOOO0O0O000O00OO +O0OOO000OOOO0OO00 )*(OOOOO0O0O000O00OO +OO000OOOO0O0O00OO )>0 :#line:545
            O000000000OOOO000 =OOOOO0O0O000O00OO *(OOOOO0O0O000O00OO +O0OOO000OOOO0OO00 +OO000OOOO0O0O00OO +O0O0O00O0O0OO000O )/(OOOOO0O0O000O00OO +O0OOO000OOOO0OO00 )/(OOOOO0O0O000O00OO +OO000OOOO0O0O00OO )-1 #line:546
        else :#line:547
            O000000000OOOO000 =None #line:548
        O00O00OOOO0000OO0 =0 #line:549
        if (OOOOO0O0O000O00OO +O0OOO000OOOO0OO00 )*(OOOOO0O0O000O00OO +OO000OOOO0O0O00OO )>0 :#line:550
            O00O00OOOO0000OO0 =1 -OOOOO0O0O000O00OO *(OOOOO0O0O000O00OO +O0OOO000OOOO0OO00 +OO000OOOO0O0O00OO +O0O0O00O0O0OO000O )/(OOOOO0O0O000O00OO +O0OOO000OOOO0OO00 )/(OOOOO0O0O000O00OO +OO000OOOO0O0O00OO )#line:551
        else :#line:552
            O00O00OOOO0000OO0 =None #line:553
        O0000O0O0O00O0OO0 =True #line:554
        for O00OO0OOOO00O0000 in OO0OO0000OO00O000 .quantifiers .keys ():#line:555
            if O00OO0OOOO00O0000 .upper ()=='BASE':#line:556
                O0000O0O0O00O0OO0 =O0000O0O0O00O0OO0 and (OO0OO0000OO00O000 .quantifiers .get (O00OO0OOOO00O0000 )<=OO0OO0OOO0000OOO0 )#line:557
            if O00OO0OOOO00O0000 .upper ()=='RELBASE':#line:558
                O0000O0O0O00O0OO0 =O0000O0O0O00O0OO0 and (OO0OO0000OO00O000 .quantifiers .get (O00OO0OOOO00O0000 )<=OO0OO0OOO0000OOO0 *1.0 /OO0OO0000OO00O000 .data ["rows_count"])#line:559
            if (O00OO0OOOO00O0000 .upper ()=='PIM')or (O00OO0OOOO00O0000 .upper ()=='CONF'):#line:560
                O0000O0O0O00O0OO0 =O0000O0O0O00O0OO0 and (OO0OO0000OO00O000 .quantifiers .get (O00OO0OOOO00O0000 )<=OOOOO00O0O0O0000O )#line:561
            if O00OO0OOOO00O0000 .upper ()=='AAD':#line:562
                if O000000000OOOO000 !=None :#line:563
                    O0000O0O0O00O0OO0 =O0000O0O0O00O0OO0 and (OO0OO0000OO00O000 .quantifiers .get (O00OO0OOOO00O0000 )<=O000000000OOOO000 )#line:564
                else :#line:565
                    O0000O0O0O00O0OO0 =False #line:566
            if O00OO0OOOO00O0000 .upper ()=='BAD':#line:567
                if O00O00OOOO0000OO0 !=None :#line:568
                    O0000O0O0O00O0OO0 =O0000O0O0O00O0OO0 and (OO0OO0000OO00O000 .quantifiers .get (O00OO0OOOO00O0000 )<=O00O00OOOO0000OO0 )#line:569
                else :#line:570
                    O0000O0O0O00O0OO0 =False #line:571
            O000OO0000OOOOOO0 ={}#line:572
        if O0000O0O0O00O0OO0 ==True :#line:573
            OO0OO0000OO00O000 .stats ['total_valid']+=1 #line:575
            O000OO0000OOOOOO0 ["base"]=OO0OO0OOO0000OOO0 #line:576
            O000OO0000OOOOOO0 ["rel_base"]=OO0OO0OOO0000OOO0 *1.0 /OO0OO0000OO00O000 .data ["rows_count"]#line:577
            O000OO0000OOOOOO0 ["conf"]=OOOOO00O0O0O0000O #line:578
            O000OO0000OOOOOO0 ["aad"]=O000000000OOOO000 #line:579
            O000OO0000OOOOOO0 ["bad"]=O00O00OOOO0000OO0 #line:580
            O000OO0000OOOOOO0 ["fourfold"]=[OOOOO0O0O000O00OO ,O0OOO000OOOO0OO00 ,OO000OOOO0O0O00OO ,O0O0O00O0O0OO000O ]#line:581
        return O0000O0O0O00O0OO0 ,O000OO0000OOOOOO0 #line:585
    def _verifysd4ft (O00OO0OO0O0000O0O ,_O0OO0O000O0O0OO00 ):#line:587
        O0000O0O0OOO0O00O ={}#line:588
        OO0O0OOOO000O0000 =0 #line:589
        for O0OOOOO00OO0000OO in O00OO0OO0O0000O0O .task_actinfo ['cedents']:#line:590
            O0000O0O0OOO0O00O [O0OOOOO00OO0000OO ['cedent_type']]=O0OOOOO00OO0000OO ['filter_value']#line:592
            OO0O0OOOO000O0000 =OO0O0OOOO000O0000 +1 #line:593
        OO00O00OOOO0O0O00 =O00OO0OO0O0000O0O ._bitcount (O0000O0O0OOO0O00O ['ante']&O0000O0O0OOO0O00O ['succ']&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['frst'])#line:595
        O0000000000O00O0O =O00OO0OO0O0000O0O ._bitcount (O0000O0O0OOO0O00O ['ante']&O0000O0O0OOO0O00O ['succ']&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['scnd'])#line:596
        OOO00OO0O00OOOO0O =None #line:597
        OO00O0OOO00OOO00O =0 #line:598
        OOO00OO000OOO0000 =0 #line:599
        if OO00O00OOOO0O0O00 >0 :#line:608
            OO00O0OOO00OOO00O =O00OO0OO0O0000O0O ._bitcount (O0000O0O0OOO0O00O ['ante']&O0000O0O0OOO0O00O ['succ']&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['frst'])*1.0 /O00OO0OO0O0000O0O ._bitcount (O0000O0O0OOO0O00O ['ante']&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['frst'])#line:609
        if O0000000000O00O0O >0 :#line:610
            OOO00OO000OOO0000 =O00OO0OO0O0000O0O ._bitcount (O0000O0O0OOO0O00O ['ante']&O0000O0O0OOO0O00O ['succ']&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['scnd'])*1.0 /O00OO0OO0O0000O0O ._bitcount (O0000O0O0OOO0O00O ['ante']&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['scnd'])#line:611
        O0O0O00O0O0OOOO0O =1 <<O00OO0OO0O0000O0O .data ["rows_count"]#line:613
        OO00OOO00000OOOO0 =O00OO0OO0O0000O0O ._bitcount (O0000O0O0OOO0O00O ['ante']&O0000O0O0OOO0O00O ['succ']&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['frst'])#line:614
        O0O00000O000O00O0 =O00OO0OO0O0000O0O ._bitcount (O0000O0O0OOO0O00O ['ante']&~(O0O0O00O0O0OOOO0O |O0000O0O0OOO0O00O ['succ'])&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['frst'])#line:615
        OO0O0O0O0OO0OOOO0 =O00OO0OO0O0000O0O ._bitcount (~(O0O0O00O0O0OOOO0O |O0000O0O0OOO0O00O ['ante'])&O0000O0O0OOO0O00O ['succ']&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['frst'])#line:616
        OOO000O00OOOOO0OO =O00OO0OO0O0000O0O ._bitcount (~(O0O0O00O0O0OOOO0O |O0000O0O0OOO0O00O ['ante'])&~(O0O0O00O0O0OOOO0O |O0000O0O0OOO0O00O ['succ'])&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['frst'])#line:617
        O0OO000OOOO0OOO00 =O00OO0OO0O0000O0O ._bitcount (O0000O0O0OOO0O00O ['ante']&O0000O0O0OOO0O00O ['succ']&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['scnd'])#line:618
        OOO0O0O00O000O0OO =O00OO0OO0O0000O0O ._bitcount (O0000O0O0OOO0O00O ['ante']&~(O0O0O00O0O0OOOO0O |O0000O0O0OOO0O00O ['succ'])&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['scnd'])#line:619
        O0O0O0OO00O0OOO0O =O00OO0OO0O0000O0O ._bitcount (~(O0O0O00O0O0OOOO0O |O0000O0O0OOO0O00O ['ante'])&O0000O0O0OOO0O00O ['succ']&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['scnd'])#line:620
        OOOO000000O0OO0OO =O00OO0OO0O0000O0O ._bitcount (~(O0O0O00O0O0OOOO0O |O0000O0O0OOO0O00O ['ante'])&~(O0O0O00O0O0OOOO0O |O0000O0O0OOO0O00O ['succ'])&O0000O0O0OOO0O00O ['cond']&O0000O0O0OOO0O00O ['scnd'])#line:621
        O00OO0000O0O000O0 =True #line:622
        for O00O0O00O00OOOO0O in O00OO0OO0O0000O0O .quantifiers .keys ():#line:623
            if (O00O0O00O00OOOO0O .upper ()=='FRSTBASE')|(O00O0O00O00OOOO0O .upper ()=='BASE1'):#line:624
                O00OO0000O0O000O0 =O00OO0000O0O000O0 and (O00OO0OO0O0000O0O .quantifiers .get (O00O0O00O00OOOO0O )<=OO00O00OOOO0O0O00 )#line:625
            if (O00O0O00O00OOOO0O .upper ()=='SCNDBASE')|(O00O0O00O00OOOO0O .upper ()=='BASE2'):#line:626
                O00OO0000O0O000O0 =O00OO0000O0O000O0 and (O00OO0OO0O0000O0O .quantifiers .get (O00O0O00O00OOOO0O )<=O0000000000O00O0O )#line:627
            if (O00O0O00O00OOOO0O .upper ()=='FRSTRELBASE')|(O00O0O00O00OOOO0O .upper ()=='RELBASE1'):#line:628
                O00OO0000O0O000O0 =O00OO0000O0O000O0 and (O00OO0OO0O0000O0O .quantifiers .get (O00O0O00O00OOOO0O )<=OO00O00OOOO0O0O00 *1.0 /O00OO0OO0O0000O0O .data ["rows_count"])#line:629
            if (O00O0O00O00OOOO0O .upper ()=='SCNDRELBASE')|(O00O0O00O00OOOO0O .upper ()=='RELBASE2'):#line:630
                O00OO0000O0O000O0 =O00OO0000O0O000O0 and (O00OO0OO0O0000O0O .quantifiers .get (O00O0O00O00OOOO0O )<=O0000000000O00O0O *1.0 /O00OO0OO0O0000O0O .data ["rows_count"])#line:631
            if (O00O0O00O00OOOO0O .upper ()=='FRSTPIM')|(O00O0O00O00OOOO0O .upper ()=='PIM1')|(O00O0O00O00OOOO0O .upper ()=='FRSTCONF')|(O00O0O00O00OOOO0O .upper ()=='CONF1'):#line:632
                O00OO0000O0O000O0 =O00OO0000O0O000O0 and (O00OO0OO0O0000O0O .quantifiers .get (O00O0O00O00OOOO0O )<=OO00O0OOO00OOO00O )#line:633
            if (O00O0O00O00OOOO0O .upper ()=='SCNDPIM')|(O00O0O00O00OOOO0O .upper ()=='PIM2')|(O00O0O00O00OOOO0O .upper ()=='SCNDCONF')|(O00O0O00O00OOOO0O .upper ()=='CONF2'):#line:634
                O00OO0000O0O000O0 =O00OO0000O0O000O0 and (O00OO0OO0O0000O0O .quantifiers .get (O00O0O00O00OOOO0O )<=OOO00OO000OOO0000 )#line:635
            if (O00O0O00O00OOOO0O .upper ()=='DELTAPIM')|(O00O0O00O00OOOO0O .upper ()=='DELTACONF'):#line:636
                O00OO0000O0O000O0 =O00OO0000O0O000O0 and (O00OO0OO0O0000O0O .quantifiers .get (O00O0O00O00OOOO0O )<=OO00O0OOO00OOO00O -OOO00OO000OOO0000 )#line:637
            if (O00O0O00O00OOOO0O .upper ()=='RATIOPIM')|(O00O0O00O00OOOO0O .upper ()=='RATIOCONF'):#line:640
                if (OOO00OO000OOO0000 >0 ):#line:641
                    O00OO0000O0O000O0 =O00OO0000O0O000O0 and (O00OO0OO0O0000O0O .quantifiers .get (O00O0O00O00OOOO0O )<=OO00O0OOO00OOO00O *1.0 /OOO00OO000OOO0000 )#line:642
                else :#line:643
                    O00OO0000O0O000O0 =False #line:644
            if (O00O0O00O00OOOO0O .upper ()=='RATIOPIM_LEQ')|(O00O0O00O00OOOO0O .upper ()=='RATIOCONF_LEQ'):#line:645
                if (OOO00OO000OOO0000 >0 ):#line:646
                    O00OO0000O0O000O0 =O00OO0000O0O000O0 and (O00OO0OO0O0000O0O .quantifiers .get (O00O0O00O00OOOO0O )>=OO00O0OOO00OOO00O *1.0 /OOO00OO000OOO0000 )#line:647
                else :#line:648
                    O00OO0000O0O000O0 =False #line:649
        O00OOO0O000000O0O ={}#line:650
        if O00OO0000O0O000O0 ==True :#line:651
            O00OO0OO0O0000O0O .stats ['total_valid']+=1 #line:653
            O00OOO0O000000O0O ["base1"]=OO00O00OOOO0O0O00 #line:654
            O00OOO0O000000O0O ["base2"]=O0000000000O00O0O #line:655
            O00OOO0O000000O0O ["rel_base1"]=OO00O00OOOO0O0O00 *1.0 /O00OO0OO0O0000O0O .data ["rows_count"]#line:656
            O00OOO0O000000O0O ["rel_base2"]=O0000000000O00O0O *1.0 /O00OO0OO0O0000O0O .data ["rows_count"]#line:657
            O00OOO0O000000O0O ["conf1"]=OO00O0OOO00OOO00O #line:658
            O00OOO0O000000O0O ["conf2"]=OOO00OO000OOO0000 #line:659
            O00OOO0O000000O0O ["deltaconf"]=OO00O0OOO00OOO00O -OOO00OO000OOO0000 #line:660
            if (OOO00OO000OOO0000 >0 ):#line:661
                O00OOO0O000000O0O ["ratioconf"]=OO00O0OOO00OOO00O *1.0 /OOO00OO000OOO0000 #line:662
            else :#line:663
                O00OOO0O000000O0O ["ratioconf"]=None #line:664
            O00OOO0O000000O0O ["fourfold1"]=[OO00OOO00000OOOO0 ,O0O00000O000O00O0 ,OO0O0O0O0OO0OOOO0 ,OOO000O00OOOOO0OO ]#line:665
            O00OOO0O000000O0O ["fourfold2"]=[O0OO000OOOO0OOO00 ,OOO0O0O00O000O0OO ,O0O0O0OO00O0OOO0O ,OOOO000000O0OO0OO ]#line:666
        return O00OO0000O0O000O0 ,O00OOO0O000000O0O #line:670
    def _verifynewact4ft (OOO00OO000O0OOOOO ,_O00OOOO0O000O000O ):#line:672
        O0OO0O0OO00000000 ={}#line:673
        for OOO00OO000OOO0OOO in OOO00OO000O0OOOOO .task_actinfo ['cedents']:#line:674
            O0OO0O0OO00000000 [OOO00OO000OOO0OOO ['cedent_type']]=OOO00OO000OOO0OOO ['filter_value']#line:676
        OOO0O0O00O0OO0O0O =OOO00OO000O0OOOOO ._bitcount (O0OO0O0OO00000000 ['ante']&O0OO0O0OO00000000 ['succ']&O0OO0O0OO00000000 ['cond'])#line:678
        O00O00OO0000O00O0 =OOO00OO000O0OOOOO ._bitcount (O0OO0O0OO00000000 ['ante']&O0OO0O0OO00000000 ['succ']&O0OO0O0OO00000000 ['cond']&O0OO0O0OO00000000 ['antv']&O0OO0O0OO00000000 ['sucv'])#line:679
        OOOO00OOO0OO0OO00 =None #line:680
        OO0O0O0OO0000O0OO =0 #line:681
        OO0OO0OOO000O00O0 =0 #line:682
        if OOO0O0O00O0OO0O0O >0 :#line:691
            OO0O0O0OO0000O0OO =OOO00OO000O0OOOOO ._bitcount (O0OO0O0OO00000000 ['ante']&O0OO0O0OO00000000 ['succ']&O0OO0O0OO00000000 ['cond'])*1.0 /OOO00OO000O0OOOOO ._bitcount (O0OO0O0OO00000000 ['ante']&O0OO0O0OO00000000 ['cond'])#line:692
        if O00O00OO0000O00O0 >0 :#line:693
            OO0OO0OOO000O00O0 =OOO00OO000O0OOOOO ._bitcount (O0OO0O0OO00000000 ['ante']&O0OO0O0OO00000000 ['succ']&O0OO0O0OO00000000 ['cond']&O0OO0O0OO00000000 ['antv']&O0OO0O0OO00000000 ['sucv'])*1.0 /OOO00OO000O0OOOOO ._bitcount (O0OO0O0OO00000000 ['ante']&O0OO0O0OO00000000 ['cond']&O0OO0O0OO00000000 ['antv'])#line:695
        O0OO0O0000OOOO0O0 =1 <<OOO00OO000O0OOOOO .rows_count #line:697
        OOOO0OOOO0OOOO0O0 =OOO00OO000O0OOOOO ._bitcount (O0OO0O0OO00000000 ['ante']&O0OO0O0OO00000000 ['succ']&O0OO0O0OO00000000 ['cond'])#line:698
        O0O000OOOO0OO0OOO =OOO00OO000O0OOOOO ._bitcount (O0OO0O0OO00000000 ['ante']&~(O0OO0O0000OOOO0O0 |O0OO0O0OO00000000 ['succ'])&O0OO0O0OO00000000 ['cond'])#line:699
        OOO0000O0O00000O0 =OOO00OO000O0OOOOO ._bitcount (~(O0OO0O0000OOOO0O0 |O0OO0O0OO00000000 ['ante'])&O0OO0O0OO00000000 ['succ']&O0OO0O0OO00000000 ['cond'])#line:700
        OOO0O000O00OOOO00 =OOO00OO000O0OOOOO ._bitcount (~(O0OO0O0000OOOO0O0 |O0OO0O0OO00000000 ['ante'])&~(O0OO0O0000OOOO0O0 |O0OO0O0OO00000000 ['succ'])&O0OO0O0OO00000000 ['cond'])#line:701
        OO000O0O000O0OOOO =OOO00OO000O0OOOOO ._bitcount (O0OO0O0OO00000000 ['ante']&O0OO0O0OO00000000 ['succ']&O0OO0O0OO00000000 ['cond']&O0OO0O0OO00000000 ['antv']&O0OO0O0OO00000000 ['sucv'])#line:702
        OOO000O00OOO0000O =OOO00OO000O0OOOOO ._bitcount (O0OO0O0OO00000000 ['ante']&~(O0OO0O0000OOOO0O0 |(O0OO0O0OO00000000 ['succ']&O0OO0O0OO00000000 ['sucv']))&O0OO0O0OO00000000 ['cond'])#line:703
        O0OOOO0O0OOO00OOO =OOO00OO000O0OOOOO ._bitcount (~(O0OO0O0000OOOO0O0 |(O0OO0O0OO00000000 ['ante']&O0OO0O0OO00000000 ['antv']))&O0OO0O0OO00000000 ['succ']&O0OO0O0OO00000000 ['cond']&O0OO0O0OO00000000 ['sucv'])#line:704
        O000O0OO00OO00OO0 =OOO00OO000O0OOOOO ._bitcount (~(O0OO0O0000OOOO0O0 |(O0OO0O0OO00000000 ['ante']&O0OO0O0OO00000000 ['antv']))&~(O0OO0O0000OOOO0O0 |(O0OO0O0OO00000000 ['succ']&O0OO0O0OO00000000 ['sucv']))&O0OO0O0OO00000000 ['cond'])#line:705
        O0OOO0OOOOOO000O0 =True #line:706
        for OO0OOOO0O0OOOO0OO in OOO00OO000O0OOOOO .quantifiers .keys ():#line:707
            if (OO0OOOO0O0OOOO0OO =='PreBase')|(OO0OOOO0O0OOOO0OO =='Base1'):#line:708
                O0OOO0OOOOOO000O0 =O0OOO0OOOOOO000O0 and (OOO00OO000O0OOOOO .quantifiers .get (OO0OOOO0O0OOOO0OO )<=OOO0O0O00O0OO0O0O )#line:709
            if (OO0OOOO0O0OOOO0OO =='PostBase')|(OO0OOOO0O0OOOO0OO =='Base2'):#line:710
                O0OOO0OOOOOO000O0 =O0OOO0OOOOOO000O0 and (OOO00OO000O0OOOOO .quantifiers .get (OO0OOOO0O0OOOO0OO )<=O00O00OO0000O00O0 )#line:711
            if (OO0OOOO0O0OOOO0OO =='PreRelBase')|(OO0OOOO0O0OOOO0OO =='RelBase1'):#line:712
                O0OOO0OOOOOO000O0 =O0OOO0OOOOOO000O0 and (OOO00OO000O0OOOOO .quantifiers .get (OO0OOOO0O0OOOO0OO )<=OOO0O0O00O0OO0O0O *1.0 /OOO00OO000O0OOOOO .data ["rows_count"])#line:713
            if (OO0OOOO0O0OOOO0OO =='PostRelBase')|(OO0OOOO0O0OOOO0OO =='RelBase2'):#line:714
                O0OOO0OOOOOO000O0 =O0OOO0OOOOOO000O0 and (OOO00OO000O0OOOOO .quantifiers .get (OO0OOOO0O0OOOO0OO )<=O00O00OO0000O00O0 *1.0 /OOO00OO000O0OOOOO .data ["rows_count"])#line:715
            if (OO0OOOO0O0OOOO0OO =='Prepim')|(OO0OOOO0O0OOOO0OO =='pim1')|(OO0OOOO0O0OOOO0OO =='PreConf')|(OO0OOOO0O0OOOO0OO =='conf1'):#line:716
                O0OOO0OOOOOO000O0 =O0OOO0OOOOOO000O0 and (OOO00OO000O0OOOOO .quantifiers .get (OO0OOOO0O0OOOO0OO )<=OO0O0O0OO0000O0OO )#line:717
            if (OO0OOOO0O0OOOO0OO =='Postpim')|(OO0OOOO0O0OOOO0OO =='pim2')|(OO0OOOO0O0OOOO0OO =='PostConf')|(OO0OOOO0O0OOOO0OO =='conf2'):#line:718
                O0OOO0OOOOOO000O0 =O0OOO0OOOOOO000O0 and (OOO00OO000O0OOOOO .quantifiers .get (OO0OOOO0O0OOOO0OO )<=OO0OO0OOO000O00O0 )#line:719
            if (OO0OOOO0O0OOOO0OO =='Deltapim')|(OO0OOOO0O0OOOO0OO =='DeltaConf'):#line:720
                O0OOO0OOOOOO000O0 =O0OOO0OOOOOO000O0 and (OOO00OO000O0OOOOO .quantifiers .get (OO0OOOO0O0OOOO0OO )<=OO0O0O0OO0000O0OO -OO0OO0OOO000O00O0 )#line:721
            if (OO0OOOO0O0OOOO0OO =='Ratiopim')|(OO0OOOO0O0OOOO0OO =='RatioConf'):#line:724
                if (OO0OO0OOO000O00O0 >0 ):#line:725
                    O0OOO0OOOOOO000O0 =O0OOO0OOOOOO000O0 and (OOO00OO000O0OOOOO .quantifiers .get (OO0OOOO0O0OOOO0OO )<=OO0O0O0OO0000O0OO *1.0 /OO0OO0OOO000O00O0 )#line:726
                else :#line:727
                    O0OOO0OOOOOO000O0 =False #line:728
        O0O0O00O00O000OO0 ={}#line:729
        if O0OOO0OOOOOO000O0 ==True :#line:730
            OOO00OO000O0OOOOO .stats ['total_valid']+=1 #line:732
            O0O0O00O00O000OO0 ["base1"]=OOO0O0O00O0OO0O0O #line:733
            O0O0O00O00O000OO0 ["base2"]=O00O00OO0000O00O0 #line:734
            O0O0O00O00O000OO0 ["rel_base1"]=OOO0O0O00O0OO0O0O *1.0 /OOO00OO000O0OOOOO .data ["rows_count"]#line:735
            O0O0O00O00O000OO0 ["rel_base2"]=O00O00OO0000O00O0 *1.0 /OOO00OO000O0OOOOO .data ["rows_count"]#line:736
            O0O0O00O00O000OO0 ["conf1"]=OO0O0O0OO0000O0OO #line:737
            O0O0O00O00O000OO0 ["conf2"]=OO0OO0OOO000O00O0 #line:738
            O0O0O00O00O000OO0 ["deltaconf"]=OO0O0O0OO0000O0OO -OO0OO0OOO000O00O0 #line:739
            if (OO0OO0OOO000O00O0 >0 ):#line:740
                O0O0O00O00O000OO0 ["ratioconf"]=OO0O0O0OO0000O0OO *1.0 /OO0OO0OOO000O00O0 #line:741
            else :#line:742
                O0O0O00O00O000OO0 ["ratioconf"]=None #line:743
            O0O0O00O00O000OO0 ["fourfoldpre"]=[OOOO0OOOO0OOOO0O0 ,O0O000OOOO0OO0OOO ,OOO0000O0O00000O0 ,OOO0O000O00OOOO00 ]#line:744
            O0O0O00O00O000OO0 ["fourfoldpost"]=[OO000O0O000O0OOOO ,OOO000O00OOO0000O ,O0OOOO0O0OOO00OOO ,O000O0OO00OO00OO0 ]#line:745
        return O0OOO0OOOOOO000O0 ,O0O0O00O00O000OO0 #line:747
    def _verifyact4ft (OO000OOO000OOO0OO ,_O0OOO00OOOO000OOO ):#line:749
        O0OOO0O0O0O00OO0O ={}#line:750
        for O00000O000000O0OO in OO000OOO000OOO0OO .task_actinfo ['cedents']:#line:751
            O0OOO0O0O0O00OO0O [O00000O000000O0OO ['cedent_type']]=O00000O000000O0OO ['filter_value']#line:753
        OO0OO00OOOOOOOO0O =OO000OOO000OOO0OO ._bitcount (O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['cond']&O0OOO0O0O0O00OO0O ['antv-']&O0OOO0O0O0O00OO0O ['sucv-'])#line:755
        O000OO0O000000OO0 =OO000OOO000OOO0OO ._bitcount (O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['cond']&O0OOO0O0O0O00OO0O ['antv+']&O0OOO0O0O0O00OO0O ['sucv+'])#line:756
        O00O00O00O0OO0OOO =None #line:757
        OOOOOO0O000OO00O0 =0 #line:758
        OO0O0O0O000OO0OOO =0 #line:759
        if OO0OO00OOOOOOOO0O >0 :#line:768
            OOOOOO0O000OO00O0 =OO000OOO000OOO0OO ._bitcount (O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['cond']&O0OOO0O0O0O00OO0O ['antv-']&O0OOO0O0O0O00OO0O ['sucv-'])*1.0 /OO000OOO000OOO0OO ._bitcount (O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['cond']&O0OOO0O0O0O00OO0O ['antv-'])#line:770
        if O000OO0O000000OO0 >0 :#line:771
            OO0O0O0O000OO0OOO =OO000OOO000OOO0OO ._bitcount (O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['cond']&O0OOO0O0O0O00OO0O ['antv+']&O0OOO0O0O0O00OO0O ['sucv+'])*1.0 /OO000OOO000OOO0OO ._bitcount (O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['cond']&O0OOO0O0O0O00OO0O ['antv+'])#line:773
        OOO0O000O0O0O0O0O =1 <<OO000OOO000OOO0OO .data ["rows_count"]#line:775
        OOOOO0OOO0OO0000O =OO000OOO000OOO0OO ._bitcount (O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['cond']&O0OOO0O0O0O00OO0O ['antv-']&O0OOO0O0O0O00OO0O ['sucv-'])#line:776
        O0O0O0OO00OO00O0O =OO000OOO000OOO0OO ._bitcount (O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['antv-']&~(OOO0O000O0O0O0O0O |(O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['sucv-']))&O0OOO0O0O0O00OO0O ['cond'])#line:777
        OOO0O0O00OOO00000 =OO000OOO000OOO0OO ._bitcount (~(OOO0O000O0O0O0O0O |(O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['antv-']))&O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['cond']&O0OOO0O0O0O00OO0O ['sucv-'])#line:778
        O0000O0OO0OOO00OO =OO000OOO000OOO0OO ._bitcount (~(OOO0O000O0O0O0O0O |(O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['antv-']))&~(OOO0O000O0O0O0O0O |(O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['sucv-']))&O0OOO0O0O0O00OO0O ['cond'])#line:779
        OO0000O000O0OOOO0 =OO000OOO000OOO0OO ._bitcount (O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['cond']&O0OOO0O0O0O00OO0O ['antv+']&O0OOO0O0O0O00OO0O ['sucv+'])#line:780
        OOOOO00OOOOOO0OOO =OO000OOO000OOO0OO ._bitcount (O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['antv+']&~(OOO0O000O0O0O0O0O |(O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['sucv+']))&O0OOO0O0O0O00OO0O ['cond'])#line:781
        OOOO0OO00O0O0O000 =OO000OOO000OOO0OO ._bitcount (~(OOO0O000O0O0O0O0O |(O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['antv+']))&O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['cond']&O0OOO0O0O0O00OO0O ['sucv+'])#line:782
        O00OO0OO0OOO0OO00 =OO000OOO000OOO0OO ._bitcount (~(OOO0O000O0O0O0O0O |(O0OOO0O0O0O00OO0O ['ante']&O0OOO0O0O0O00OO0O ['antv+']))&~(OOO0O000O0O0O0O0O |(O0OOO0O0O0O00OO0O ['succ']&O0OOO0O0O0O00OO0O ['sucv+']))&O0OOO0O0O0O00OO0O ['cond'])#line:783
        O00O00O00O000O00O =True #line:784
        for O0OO0OOO0O0O0000O in OO000OOO000OOO0OO .quantifiers .keys ():#line:785
            if (O0OO0OOO0O0O0000O =='PreBase')|(O0OO0OOO0O0O0000O =='Base1'):#line:786
                O00O00O00O000O00O =O00O00O00O000O00O and (OO000OOO000OOO0OO .quantifiers .get (O0OO0OOO0O0O0000O )<=OO0OO00OOOOOOOO0O )#line:787
            if (O0OO0OOO0O0O0000O =='PostBase')|(O0OO0OOO0O0O0000O =='Base2'):#line:788
                O00O00O00O000O00O =O00O00O00O000O00O and (OO000OOO000OOO0OO .quantifiers .get (O0OO0OOO0O0O0000O )<=O000OO0O000000OO0 )#line:789
            if (O0OO0OOO0O0O0000O =='PreRelBase')|(O0OO0OOO0O0O0000O =='RelBase1'):#line:790
                O00O00O00O000O00O =O00O00O00O000O00O and (OO000OOO000OOO0OO .quantifiers .get (O0OO0OOO0O0O0000O )<=OO0OO00OOOOOOOO0O *1.0 /OO000OOO000OOO0OO .data ["rows_count"])#line:791
            if (O0OO0OOO0O0O0000O =='PostRelBase')|(O0OO0OOO0O0O0000O =='RelBase2'):#line:792
                O00O00O00O000O00O =O00O00O00O000O00O and (OO000OOO000OOO0OO .quantifiers .get (O0OO0OOO0O0O0000O )<=O000OO0O000000OO0 *1.0 /OO000OOO000OOO0OO .data ["rows_count"])#line:793
            if (O0OO0OOO0O0O0000O =='Prepim')|(O0OO0OOO0O0O0000O =='pim1')|(O0OO0OOO0O0O0000O =='PreConf')|(O0OO0OOO0O0O0000O =='conf1'):#line:794
                O00O00O00O000O00O =O00O00O00O000O00O and (OO000OOO000OOO0OO .quantifiers .get (O0OO0OOO0O0O0000O )<=OOOOOO0O000OO00O0 )#line:795
            if (O0OO0OOO0O0O0000O =='Postpim')|(O0OO0OOO0O0O0000O =='pim2')|(O0OO0OOO0O0O0000O =='PostConf')|(O0OO0OOO0O0O0000O =='conf2'):#line:796
                O00O00O00O000O00O =O00O00O00O000O00O and (OO000OOO000OOO0OO .quantifiers .get (O0OO0OOO0O0O0000O )<=OO0O0O0O000OO0OOO )#line:797
            if (O0OO0OOO0O0O0000O =='Deltapim')|(O0OO0OOO0O0O0000O =='DeltaConf'):#line:798
                O00O00O00O000O00O =O00O00O00O000O00O and (OO000OOO000OOO0OO .quantifiers .get (O0OO0OOO0O0O0000O )<=OOOOOO0O000OO00O0 -OO0O0O0O000OO0OOO )#line:799
            if (O0OO0OOO0O0O0000O =='Ratiopim')|(O0OO0OOO0O0O0000O =='RatioConf'):#line:802
                if (OOOOOO0O000OO00O0 >0 ):#line:803
                    O00O00O00O000O00O =O00O00O00O000O00O and (OO000OOO000OOO0OO .quantifiers .get (O0OO0OOO0O0O0000O )<=OO0O0O0O000OO0OOO *1.0 /OOOOOO0O000OO00O0 )#line:804
                else :#line:805
                    O00O00O00O000O00O =False #line:806
        O0O0OO0O0000O00OO ={}#line:807
        if O00O00O00O000O00O ==True :#line:808
            OO000OOO000OOO0OO .stats ['total_valid']+=1 #line:810
            O0O0OO0O0000O00OO ["base1"]=OO0OO00OOOOOOOO0O #line:811
            O0O0OO0O0000O00OO ["base2"]=O000OO0O000000OO0 #line:812
            O0O0OO0O0000O00OO ["rel_base1"]=OO0OO00OOOOOOOO0O *1.0 /OO000OOO000OOO0OO .data ["rows_count"]#line:813
            O0O0OO0O0000O00OO ["rel_base2"]=O000OO0O000000OO0 *1.0 /OO000OOO000OOO0OO .data ["rows_count"]#line:814
            O0O0OO0O0000O00OO ["conf1"]=OOOOOO0O000OO00O0 #line:815
            O0O0OO0O0000O00OO ["conf2"]=OO0O0O0O000OO0OOO #line:816
            O0O0OO0O0000O00OO ["deltaconf"]=OOOOOO0O000OO00O0 -OO0O0O0O000OO0OOO #line:817
            if (OOOOOO0O000OO00O0 >0 ):#line:818
                O0O0OO0O0000O00OO ["ratioconf"]=OO0O0O0O000OO0OOO *1.0 /OOOOOO0O000OO00O0 #line:819
            else :#line:820
                O0O0OO0O0000O00OO ["ratioconf"]=None #line:821
            O0O0OO0O0000O00OO ["fourfoldpre"]=[OOOOO0OOO0OO0000O ,O0O0O0OO00OO00O0O ,OOO0O0O00OOO00000 ,O0000O0OO0OOO00OO ]#line:822
            O0O0OO0O0000O00OO ["fourfoldpost"]=[OO0000O000O0OOOO0 ,OOOOO00OOOOOO0OOO ,OOOO0OO00O0O0O000 ,O00OO0OO0OOO0OO00 ]#line:823
        return O00O00O00O000O00O ,O0O0OO0O0000O00OO #line:825
    def _verify_opt (OOO0OOO0OO0OOOO0O ,O0O000OOO00O0O000 ,OO0OO0O00000000OO ):#line:827
        OOO0OOO0OO0OOOO0O .stats ['total_ver']+=1 #line:828
        O00O000OOOOOOO00O =False #line:829
        if not (O0O000OOO00O0O000 ['optim'].get ('only_con')):#line:832
            return False #line:833
        if not (OOO0OOO0OO0OOOO0O .options ['optimizations']):#line:836
            return False #line:838
        O000O000OO0OOOOO0 ={}#line:840
        for OO0O0O000000O0000 in OOO0OOO0OO0OOOO0O .task_actinfo ['cedents']:#line:841
            O000O000OO0OOOOO0 [OO0O0O000000O0000 ['cedent_type']]=OO0O0O000000O0000 ['filter_value']#line:843
        OOO0000OO000O0000 =1 <<OOO0OOO0OO0OOOO0O .data ["rows_count"]#line:845
        O0OO00OOO0OO0O0OO =OOO0000OO000O0000 -1 #line:846
        OOOO00O0O00000OOO =""#line:847
        O0O00OO0OOOO0O0OO =0 #line:848
        if (O000O000OO0OOOOO0 .get ('ante')!=None ):#line:849
            O0OO00OOO0OO0O0OO =O0OO00OOO0OO0O0OO &O000O000OO0OOOOO0 ['ante']#line:850
        if (O000O000OO0OOOOO0 .get ('succ')!=None ):#line:851
            O0OO00OOO0OO0O0OO =O0OO00OOO0OO0O0OO &O000O000OO0OOOOO0 ['succ']#line:852
        if (O000O000OO0OOOOO0 .get ('cond')!=None ):#line:853
            O0OO00OOO0OO0O0OO =O0OO00OOO0OO0O0OO &O000O000OO0OOOOO0 ['cond']#line:854
        OOO0O00O0O00OO00O =None #line:857
        if (OOO0OOO0OO0OOOO0O .proc =='CFMiner')|(OOO0OOO0OO0OOOO0O .proc =='4ftMiner')|(OOO0OOO0OO0OOOO0O .proc =='UICMiner'):#line:882
            O0OO0O000O0O0000O =OOO0OOO0OO0OOOO0O ._bitcount (O0OO00OOO0OO0O0OO )#line:883
            if not (OOO0OOO0OO0OOOO0O ._opt_base ==None ):#line:884
                if not (OOO0OOO0OO0OOOO0O ._opt_base <=O0OO0O000O0O0000O ):#line:885
                    O00O000OOOOOOO00O =True #line:886
            if not (OOO0OOO0OO0OOOO0O ._opt_relbase ==None ):#line:888
                if not (OOO0OOO0OO0OOOO0O ._opt_relbase <=O0OO0O000O0O0000O *1.0 /OOO0OOO0OO0OOOO0O .data ["rows_count"]):#line:889
                    O00O000OOOOOOO00O =True #line:890
        if (OOO0OOO0OO0OOOO0O .proc =='SD4ftMiner'):#line:892
            O0OO0O000O0O0000O =OOO0OOO0OO0OOOO0O ._bitcount (O0OO00OOO0OO0O0OO )#line:893
            if (not (OOO0OOO0OO0OOOO0O ._opt_base1 ==None ))&(not (OOO0OOO0OO0OOOO0O ._opt_base2 ==None )):#line:894
                if not (max (OOO0OOO0OO0OOOO0O ._opt_base1 ,OOO0OOO0OO0OOOO0O ._opt_base2 )<=O0OO0O000O0O0000O ):#line:895
                    O00O000OOOOOOO00O =True #line:897
            if (not (OOO0OOO0OO0OOOO0O ._opt_relbase1 ==None ))&(not (OOO0OOO0OO0OOOO0O ._opt_relbase2 ==None )):#line:898
                if not (max (OOO0OOO0OO0OOOO0O ._opt_relbase1 ,OOO0OOO0OO0OOOO0O ._opt_relbase2 )<=O0OO0O000O0O0000O *1.0 /OOO0OOO0OO0OOOO0O .data ["rows_count"]):#line:899
                    O00O000OOOOOOO00O =True #line:900
        return O00O000OOOOOOO00O #line:902
        if OOO0OOO0OO0OOOO0O .proc =='CFMiner':#line:905
            if (OO0OO0O00000000OO ['cedent_type']=='cond')&(OO0OO0O00000000OO ['defi'].get ('type')=='con'):#line:906
                O0OO0O000O0O0000O =bin (O000O000OO0OOOOO0 ['cond']).count ("1")#line:907
                OO00000O0O0OO00O0 =True #line:908
                for O00O00OOO00O0O00O in OOO0OOO0OO0OOOO0O .quantifiers .keys ():#line:909
                    if O00O00OOO00O0O00O =='Base':#line:910
                        OO00000O0O0OO00O0 =OO00000O0O0OO00O0 and (OOO0OOO0OO0OOOO0O .quantifiers .get (O00O00OOO00O0O00O )<=O0OO0O000O0O0000O )#line:911
                        if not (OO00000O0O0OO00O0 ):#line:912
                            print (f"...optimization : base is {O0OO0O000O0O0000O} for {OO0OO0O00000000OO['generated_string']}")#line:913
                    if O00O00OOO00O0O00O =='RelBase':#line:914
                        OO00000O0O0OO00O0 =OO00000O0O0OO00O0 and (OOO0OOO0OO0OOOO0O .quantifiers .get (O00O00OOO00O0O00O )<=O0OO0O000O0O0000O *1.0 /OOO0OOO0OO0OOOO0O .data ["rows_count"])#line:915
                        if not (OO00000O0O0OO00O0 ):#line:916
                            print (f"...optimization : base is {O0OO0O000O0O0000O} for {OO0OO0O00000000OO['generated_string']}")#line:917
                O00O000OOOOOOO00O =not (OO00000O0O0OO00O0 )#line:918
        elif OOO0OOO0OO0OOOO0O .proc =='4ftMiner':#line:919
            if (OO0OO0O00000000OO ['cedent_type']=='cond')&(OO0OO0O00000000OO ['defi'].get ('type')=='con'):#line:920
                O0OO0O000O0O0000O =bin (O000O000OO0OOOOO0 ['cond']).count ("1")#line:921
                OO00000O0O0OO00O0 =True #line:922
                for O00O00OOO00O0O00O in OOO0OOO0OO0OOOO0O .quantifiers .keys ():#line:923
                    if O00O00OOO00O0O00O =='Base':#line:924
                        OO00000O0O0OO00O0 =OO00000O0O0OO00O0 and (OOO0OOO0OO0OOOO0O .quantifiers .get (O00O00OOO00O0O00O )<=O0OO0O000O0O0000O )#line:925
                        if not (OO00000O0O0OO00O0 ):#line:926
                            print (f"...optimization : base is {O0OO0O000O0O0000O} for {OO0OO0O00000000OO['generated_string']}")#line:927
                    if O00O00OOO00O0O00O =='RelBase':#line:928
                        OO00000O0O0OO00O0 =OO00000O0O0OO00O0 and (OOO0OOO0OO0OOOO0O .quantifiers .get (O00O00OOO00O0O00O )<=O0OO0O000O0O0000O *1.0 /OOO0OOO0OO0OOOO0O .data ["rows_count"])#line:929
                        if not (OO00000O0O0OO00O0 ):#line:930
                            print (f"...optimization : base is {O0OO0O000O0O0000O} for {OO0OO0O00000000OO['generated_string']}")#line:931
                O00O000OOOOOOO00O =not (OO00000O0O0OO00O0 )#line:932
            if (OO0OO0O00000000OO ['cedent_type']=='ante')&(OO0OO0O00000000OO ['defi'].get ('type')=='con'):#line:933
                O0OO0O000O0O0000O =bin (O000O000OO0OOOOO0 ['ante']&O000O000OO0OOOOO0 ['cond']).count ("1")#line:934
                OO00000O0O0OO00O0 =True #line:935
                for O00O00OOO00O0O00O in OOO0OOO0OO0OOOO0O .quantifiers .keys ():#line:936
                    if O00O00OOO00O0O00O =='Base':#line:937
                        OO00000O0O0OO00O0 =OO00000O0O0OO00O0 and (OOO0OOO0OO0OOOO0O .quantifiers .get (O00O00OOO00O0O00O )<=O0OO0O000O0O0000O )#line:938
                        if not (OO00000O0O0OO00O0 ):#line:939
                            print (f"...optimization : ANTE: base is {O0OO0O000O0O0000O} for {OO0OO0O00000000OO['generated_string']}")#line:940
                    if O00O00OOO00O0O00O =='RelBase':#line:941
                        OO00000O0O0OO00O0 =OO00000O0O0OO00O0 and (OOO0OOO0OO0OOOO0O .quantifiers .get (O00O00OOO00O0O00O )<=O0OO0O000O0O0000O *1.0 /OOO0OOO0OO0OOOO0O .data ["rows_count"])#line:942
                        if not (OO00000O0O0OO00O0 ):#line:943
                            print (f"...optimization : ANTE:  base is {O0OO0O000O0O0000O} for {OO0OO0O00000000OO['generated_string']}")#line:944
                O00O000OOOOOOO00O =not (OO00000O0O0OO00O0 )#line:945
            if (OO0OO0O00000000OO ['cedent_type']=='succ')&(OO0OO0O00000000OO ['defi'].get ('type')=='con'):#line:946
                O0OO0O000O0O0000O =bin (O000O000OO0OOOOO0 ['ante']&O000O000OO0OOOOO0 ['cond']&O000O000OO0OOOOO0 ['succ']).count ("1")#line:947
                OOO0O00O0O00OO00O =0 #line:948
                if O0OO0O000O0O0000O >0 :#line:949
                    OOO0O00O0O00OO00O =bin (O000O000OO0OOOOO0 ['ante']&O000O000OO0OOOOO0 ['succ']&O000O000OO0OOOOO0 ['cond']).count ("1")*1.0 /bin (O000O000OO0OOOOO0 ['ante']&O000O000OO0OOOOO0 ['cond']).count ("1")#line:950
                OOO0000OO000O0000 =1 <<OOO0OOO0OO0OOOO0O .data ["rows_count"]#line:951
                OOOOO0OO0OO00OOOO =bin (O000O000OO0OOOOO0 ['ante']&O000O000OO0OOOOO0 ['succ']&O000O000OO0OOOOO0 ['cond']).count ("1")#line:952
                OO0O0O00O0OO0O0O0 =bin (O000O000OO0OOOOO0 ['ante']&~(OOO0000OO000O0000 |O000O000OO0OOOOO0 ['succ'])&O000O000OO0OOOOO0 ['cond']).count ("1")#line:953
                OO0O0O000000O0000 =bin (~(OOO0000OO000O0000 |O000O000OO0OOOOO0 ['ante'])&O000O000OO0OOOOO0 ['succ']&O000O000OO0OOOOO0 ['cond']).count ("1")#line:954
                O000OOO0O0O0OOO00 =bin (~(OOO0000OO000O0000 |O000O000OO0OOOOO0 ['ante'])&~(OOO0000OO000O0000 |O000O000OO0OOOOO0 ['succ'])&O000O000OO0OOOOO0 ['cond']).count ("1")#line:955
                OO00000O0O0OO00O0 =True #line:956
                for O00O00OOO00O0O00O in OOO0OOO0OO0OOOO0O .quantifiers .keys ():#line:957
                    if O00O00OOO00O0O00O =='pim':#line:958
                        OO00000O0O0OO00O0 =OO00000O0O0OO00O0 and (OOO0OOO0OO0OOOO0O .quantifiers .get (O00O00OOO00O0O00O )<=OOO0O00O0O00OO00O )#line:959
                    if not (OO00000O0O0OO00O0 ):#line:960
                        print (f"...optimization : SUCC:  pim is {OOO0O00O0O00OO00O} for {OO0OO0O00000000OO['generated_string']}")#line:961
                    if O00O00OOO00O0O00O =='aad':#line:963
                        if (OOOOO0OO0OO00OOOO +OO0O0O00O0OO0O0O0 )*(OOOOO0OO0OO00OOOO +OO0O0O000000O0000 )>0 :#line:964
                            OO00000O0O0OO00O0 =OO00000O0O0OO00O0 and (OOO0OOO0OO0OOOO0O .quantifiers .get (O00O00OOO00O0O00O )<=OOOOO0OO0OO00OOOO *(OOOOO0OO0OO00OOOO +OO0O0O00O0OO0O0O0 +OO0O0O000000O0000 +O000OOO0O0O0OOO00 )/(OOOOO0OO0OO00OOOO +OO0O0O00O0OO0O0O0 )/(OOOOO0OO0OO00OOOO +OO0O0O000000O0000 )-1 )#line:965
                        else :#line:966
                            OO00000O0O0OO00O0 =False #line:967
                        if not (OO00000O0O0OO00O0 ):#line:968
                            O000OOOOOOOOO000O =OOOOO0OO0OO00OOOO *(OOOOO0OO0OO00OOOO +OO0O0O00O0OO0O0O0 +OO0O0O000000O0000 +O000OOO0O0O0OOO00 )/(OOOOO0OO0OO00OOOO +OO0O0O00O0OO0O0O0 )/(OOOOO0OO0OO00OOOO +OO0O0O000000O0000 )-1 #line:969
                            print (f"...optimization : SUCC:  aad is {O000OOOOOOOOO000O} for {OO0OO0O00000000OO['generated_string']}")#line:970
                    if O00O00OOO00O0O00O =='bad':#line:971
                        if (OOOOO0OO0OO00OOOO +OO0O0O00O0OO0O0O0 )*(OOOOO0OO0OO00OOOO +OO0O0O000000O0000 )>0 :#line:972
                            OO00000O0O0OO00O0 =OO00000O0O0OO00O0 and (OOO0OOO0OO0OOOO0O .quantifiers .get (O00O00OOO00O0O00O )<=1 -OOOOO0OO0OO00OOOO *(OOOOO0OO0OO00OOOO +OO0O0O00O0OO0O0O0 +OO0O0O000000O0000 +O000OOO0O0O0OOO00 )/(OOOOO0OO0OO00OOOO +OO0O0O00O0OO0O0O0 )/(OOOOO0OO0OO00OOOO +OO0O0O000000O0000 ))#line:973
                        else :#line:974
                            OO00000O0O0OO00O0 =False #line:975
                        if not (OO00000O0O0OO00O0 ):#line:976
                            OOO000OO000O0O0O0 =1 -OOOOO0OO0OO00OOOO *(OOOOO0OO0OO00OOOO +OO0O0O00O0OO0O0O0 +OO0O0O000000O0000 +O000OOO0O0O0OOO00 )/(OOOOO0OO0OO00OOOO +OO0O0O00O0OO0O0O0 )/(OOOOO0OO0OO00OOOO +OO0O0O000000O0000 )#line:977
                            print (f"...optimization : SUCC:  bad is {OOO000OO000O0O0O0} for {OO0OO0O00000000OO['generated_string']}")#line:978
                O00O000OOOOOOO00O =not (OO00000O0O0OO00O0 )#line:979
        if (O00O000OOOOOOO00O ):#line:980
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {OO0OO0O00000000OO['cedent_type']}")#line:981
        return O00O000OOOOOOO00O #line:982
    def _print (OO0O0OO0O00OO0O00 ,O00000000OO0O0OOO ,_O00O0OOO0OO0OOOO0 ,_OO0O00O00O000OO00 ):#line:985
        if (len (_O00O0OOO0OO0OOOO0 ))!=len (_OO0O00O00O000OO00 ):#line:986
            print ("DIFF IN LEN for following cedent : "+str (len (_O00O0OOO0OO0OOOO0 ))+" vs "+str (len (_OO0O00O00O000OO00 )))#line:987
            print ("trace cedent : "+str (_O00O0OOO0OO0OOOO0 )+", traces "+str (_OO0O00O00O000OO00 ))#line:988
        OOOO00O000OO0OO0O =''#line:989
        O00O000000OO0O0OO ={}#line:990
        O00OOOO000O0000OO =[]#line:991
        for OO0OOOO000000OOO0 in range (len (_O00O0OOO0OO0OOOO0 )):#line:992
            O0O0OOO00OO0O000O =OO0O0OO0O00OO0O00 .data ["varname"].index (O00000000OO0O0OOO ['defi'].get ('attributes')[_O00O0OOO0OO0OOOO0 [OO0OOOO000000OOO0 ]].get ('name'))#line:993
            OOOO00O000OO0OO0O =OOOO00O000OO0OO0O +OO0O0OO0O00OO0O00 .data ["varname"][O0O0OOO00OO0O000O ]+'('#line:995
            O00OOOO000O0000OO .append (O0O0OOO00OO0O000O )#line:996
            O0O00OOO0000OOOOO =[]#line:997
            for OO000O00OOOOOOO0O in _OO0O00O00O000OO00 [OO0OOOO000000OOO0 ]:#line:998
                OOOO00O000OO0OO0O =OOOO00O000OO0OO0O +str (OO0O0OO0O00OO0O00 .data ["catnames"][O0O0OOO00OO0O000O ][OO000O00OOOOOOO0O ])+" "#line:999
                O0O00OOO0000OOOOO .append (str (OO0O0OO0O00OO0O00 .data ["catnames"][O0O0OOO00OO0O000O ][OO000O00OOOOOOO0O ]))#line:1000
            OOOO00O000OO0OO0O =OOOO00O000OO0OO0O [:-1 ]+')'#line:1001
            O00O000000OO0O0OO [OO0O0OO0O00OO0O00 .data ["varname"][O0O0OOO00OO0O000O ]]=O0O00OOO0000OOOOO #line:1002
            if OO0OOOO000000OOO0 +1 <len (_O00O0OOO0OO0OOOO0 ):#line:1003
                OOOO00O000OO0OO0O =OOOO00O000OO0OO0O +' & '#line:1004
        return OOOO00O000OO0OO0O ,O00O000000OO0O0OO ,O00OOOO000O0000OO #line:1008
    def _print_hypo (OOO00O000OO0OO00O ,OO00O0OOO0OO0OO0O ):#line:1010
        OOO00O000OO0OO00O .print_rule (OO00O0OOO0OO0OO0O )#line:1011
    def _print_rule (O00OO00O0O0OOO0OO ,OOO000OO0000OO00O ):#line:1013
        if O00OO00O0O0OOO0OO .verbosity ['print_rules']:#line:1014
            print ('Rules info : '+str (OOO000OO0000OO00O ['params']))#line:1015
            for O0OOOOO000O0OO0OO in O00OO00O0O0OOO0OO .task_actinfo ['cedents']:#line:1016
                print (O0OOOOO000O0OO0OO ['cedent_type']+' = '+O0OOOOO000O0OO0OO ['generated_string'])#line:1017
    def _genvar (OO00O0O0OO0OOOOOO ,O00OOO0O00O0O0O00 ,O00O00O0OO00OOO00 ,_OO0O0OOO00O00OO0O ,_OOOOO0OOOOOOO000O ,_O00O0O0OOO000OOOO ,_O00O0000O00O0000O ,_O0OOO00O0OO0OO0OO ):#line:1019
        for O0000OO00OOOO0O0O in range (O00O00O0OO00OOO00 ['num_cedent']):#line:1020
            if len (_OO0O0OOO00O00OO0O )==0 or O0000OO00OOOO0O0O >_OO0O0OOO00O00OO0O [-1 ]:#line:1021
                _OO0O0OOO00O00OO0O .append (O0000OO00OOOO0O0O )#line:1022
                OO0OO00O000000OO0 =OO00O0O0OO0OOOOOO .data ["varname"].index (O00O00O0OO00OOO00 ['defi'].get ('attributes')[O0000OO00OOOO0O0O ].get ('name'))#line:1023
                _OOOOOOO0OO0000OOO =O00O00O0OO00OOO00 ['defi'].get ('attributes')[O0000OO00OOOO0O0O ].get ('minlen')#line:1024
                _OOOO0O00O000O0000 =O00O00O0OO00OOO00 ['defi'].get ('attributes')[O0000OO00OOOO0O0O ].get ('maxlen')#line:1025
                _OOO0OO00OOOOOOOOO =O00O00O0OO00OOO00 ['defi'].get ('attributes')[O0000OO00OOOO0O0O ].get ('type')#line:1026
                OO000O000OO0O000O =len (OO00O0O0OO0OOOOOO .data ["dm"][OO0OO00O000000OO0 ])#line:1027
                _OOOOOOO0OO0O0O0OO =[]#line:1028
                _OOOOO0OOOOOOO000O .append (_OOOOOOO0OO0O0O0OO )#line:1029
                _OOOO000000OO0O00O =int (0 )#line:1030
                OO00O0O0OO0OOOOOO ._gencomb (O00OOO0O00O0O0O00 ,O00O00O0OO00OOO00 ,_OO0O0OOO00O00OO0O ,_OOOOO0OOOOOOO000O ,_OOOOOOO0OO0O0O0OO ,_O00O0O0OOO000OOOO ,_OOOO000000OO0O00O ,OO000O000OO0O000O ,_OOO0OO00OOOOOOOOO ,_O00O0000O00O0000O ,_O0OOO00O0OO0OO0OO ,_OOOOOOO0OO0000OOO ,_OOOO0O00O000O0000 )#line:1031
                _OOOOO0OOOOOOO000O .pop ()#line:1032
                _OO0O0OOO00O00OO0O .pop ()#line:1033
    def _gencomb (OOOO0OOOOOO00000O ,OO00O00OOOOO0O000 ,OOO000OOOO0O00OO0 ,_O00OOO0000000OO0O ,_OOO00O0OOO00000OO ,_OO000000OO00O00O0 ,_OOO0OO00OOO00OOOO ,_OOO00O0O000OOO0OO ,O0OO0O0O0OOOO00OO ,_OO0O0O00OO0000000 ,_OOO00O0O0O0O00OO0 ,_OOOOOO000O0OO00O0 ,_OO0O00O000OO0OOO0 ,_O0OOOOOO00O0000O0 ):#line:1035
        _O000O0OOO0000OOOO =[]#line:1036
        if _OO0O0O00OO0000000 =="subset":#line:1037
            if len (_OO000000OO00O00O0 )==0 :#line:1038
                _O000O0OOO0000OOOO =range (O0OO0O0O0OOOO00OO )#line:1039
            else :#line:1040
                _O000O0OOO0000OOOO =range (_OO000000OO00O00O0 [-1 ]+1 ,O0OO0O0O0OOOO00OO )#line:1041
        elif _OO0O0O00OO0000000 =="seq":#line:1042
            if len (_OO000000OO00O00O0 )==0 :#line:1043
                _O000O0OOO0000OOOO =range (O0OO0O0O0OOOO00OO -_OO0O00O000OO0OOO0 +1 )#line:1044
            else :#line:1045
                if _OO000000OO00O00O0 [-1 ]+1 ==O0OO0O0O0OOOO00OO :#line:1046
                    return #line:1047
                O000OOOOO000000OO =_OO000000OO00O00O0 [-1 ]+1 #line:1048
                _O000O0OOO0000OOOO .append (O000OOOOO000000OO )#line:1049
        elif _OO0O0O00OO0000000 =="lcut":#line:1050
            if len (_OO000000OO00O00O0 )==0 :#line:1051
                O000OOOOO000000OO =0 ;#line:1052
            else :#line:1053
                if _OO000000OO00O00O0 [-1 ]+1 ==O0OO0O0O0OOOO00OO :#line:1054
                    return #line:1055
                O000OOOOO000000OO =_OO000000OO00O00O0 [-1 ]+1 #line:1056
            _O000O0OOO0000OOOO .append (O000OOOOO000000OO )#line:1057
        elif _OO0O0O00OO0000000 =="rcut":#line:1058
            if len (_OO000000OO00O00O0 )==0 :#line:1059
                O000OOOOO000000OO =O0OO0O0O0OOOO00OO -1 ;#line:1060
            else :#line:1061
                if _OO000000OO00O00O0 [-1 ]==0 :#line:1062
                    return #line:1063
                O000OOOOO000000OO =_OO000000OO00O00O0 [-1 ]-1 #line:1064
            _O000O0OOO0000OOOO .append (O000OOOOO000000OO )#line:1066
        elif _OO0O0O00OO0000000 =="one":#line:1067
            if len (_OO000000OO00O00O0 )==0 :#line:1068
                OOOOO0000O0000OO0 =OOOO0OOOOOO00000O .data ["varname"].index (OOO000OOOO0O00OO0 ['defi'].get ('attributes')[_O00OOO0000000OO0O [-1 ]].get ('name'))#line:1069
                try :#line:1070
                    O000OOOOO000000OO =OOOO0OOOOOO00000O .data ["catnames"][OOOOO0000O0000OO0 ].index (OOO000OOOO0O00OO0 ['defi'].get ('attributes')[_O00OOO0000000OO0O [-1 ]].get ('value'))#line:1071
                except :#line:1072
                    print (f"ERROR: attribute '{OOO000OOOO0O00OO0['defi'].get('attributes')[_O00OOO0000000OO0O[-1]].get('name')}' has not value '{OOO000OOOO0O00OO0['defi'].get('attributes')[_O00OOO0000000OO0O[-1]].get('value')}'")#line:1073
                    exit (1 )#line:1074
                _O000O0OOO0000OOOO .append (O000OOOOO000000OO )#line:1075
                _OO0O00O000OO0OOO0 =1 #line:1076
                _O0OOOOOO00O0000O0 =1 #line:1077
            else :#line:1078
                print ("DEBUG: one category should not have more categories")#line:1079
                return #line:1080
        else :#line:1081
            print ("Attribute type "+_OO0O0O00OO0000000 +" not supported.")#line:1082
            return #line:1083
        for O00O000000O000000 in _O000O0OOO0000OOOO :#line:1086
                _OO000000OO00O00O0 .append (O00O000000O000000 )#line:1088
                _OOO00O0OOO00000OO .pop ()#line:1089
                _OOO00O0OOO00000OO .append (_OO000000OO00O00O0 )#line:1090
                _O00O0O0000O000OOO =_OOO00O0O000OOO0OO |OOOO0OOOOOO00000O .data ["dm"][OOOO0OOOOOO00000O .data ["varname"].index (OOO000OOOO0O00OO0 ['defi'].get ('attributes')[_O00OOO0000000OO0O [-1 ]].get ('name'))][O00O000000O000000 ]#line:1094
                _OO0OOOOOOOOO00OOO =1 #line:1096
                if (len (_O00OOO0000000OO0O )<_OOO00O0O0O0O00OO0 ):#line:1097
                    _OO0OOOOOOOOO00OOO =-1 #line:1098
                if (len (_OOO00O0OOO00000OO [-1 ])<_OO0O00O000OO0OOO0 ):#line:1100
                    _OO0OOOOOOOOO00OOO =0 #line:1101
                _O0000O0OOO000OOO0 =0 #line:1103
                if OOO000OOOO0O00OO0 ['defi'].get ('type')=='con':#line:1104
                    _O0000O0OOO000OOO0 =_OOO0OO00OOO00OOOO &_O00O0O0000O000OOO #line:1105
                else :#line:1106
                    _O0000O0OOO000OOO0 =_OOO0OO00OOO00OOOO |_O00O0O0000O000OOO #line:1107
                OOO000OOOO0O00OO0 ['trace_cedent']=_O00OOO0000000OO0O #line:1108
                OOO000OOOO0O00OO0 ['traces']=_OOO00O0OOO00000OO #line:1109
                O00O0OOOO0O0OOOOO ,O0O0OO0O000OOO0OO ,O0O0O000O0O0OOO00 =OOOO0OOOOOO00000O ._print (OOO000OOOO0O00OO0 ,_O00OOO0000000OO0O ,_OOO00O0OOO00000OO )#line:1110
                OOO000OOOO0O00OO0 ['generated_string']=O00O0OOOO0O0OOOOO #line:1111
                OOO000OOOO0O00OO0 ['rule']=O0O0OO0O000OOO0OO #line:1112
                OOO000OOOO0O00OO0 ['filter_value']=_O0000O0OOO000OOO0 #line:1113
                OOO000OOOO0O00OO0 ['traces']=copy .deepcopy (_OOO00O0OOO00000OO )#line:1114
                OOO000OOOO0O00OO0 ['trace_cedent']=copy .deepcopy (_O00OOO0000000OO0O )#line:1115
                OOO000OOOO0O00OO0 ['trace_cedent_asindata']=copy .deepcopy (O0O0O000O0O0OOO00 )#line:1116
                OO00O00OOOOO0O000 ['cedents'].append (OOO000OOOO0O00OO0 )#line:1118
                OO0000OO0O0OOO000 =OOOO0OOOOOO00000O ._verify_opt (OO00O00OOOOO0O000 ,OOO000OOOO0O00OO0 )#line:1119
                if not (OO0000OO0O0OOO000 ):#line:1125
                    if _OO0OOOOOOOOO00OOO ==1 :#line:1126
                        if len (OO00O00OOOOO0O000 ['cedents_to_do'])==len (OO00O00OOOOO0O000 ['cedents']):#line:1128
                            if OOOO0OOOOOO00000O .proc =='CFMiner':#line:1129
                                OO00O0OO0OO0O0OOO ,O0O0OO0O0O0OO0OOO =OOOO0OOOOOO00000O ._verifyCF (_O0000O0OOO000OOO0 )#line:1130
                            elif OOOO0OOOOOO00000O .proc =='UICMiner':#line:1131
                                OO00O0OO0OO0O0OOO ,O0O0OO0O0O0OO0OOO =OOOO0OOOOOO00000O ._verifyUIC (_O0000O0OOO000OOO0 )#line:1132
                            elif OOOO0OOOOOO00000O .proc =='4ftMiner':#line:1133
                                OO00O0OO0OO0O0OOO ,O0O0OO0O0O0OO0OOO =OOOO0OOOOOO00000O ._verify4ft (_O00O0O0000O000OOO )#line:1134
                            elif OOOO0OOOOOO00000O .proc =='SD4ftMiner':#line:1135
                                OO00O0OO0OO0O0OOO ,O0O0OO0O0O0OO0OOO =OOOO0OOOOOO00000O ._verifysd4ft (_O00O0O0000O000OOO )#line:1136
                            elif OOOO0OOOOOO00000O .proc =='NewAct4ftMiner':#line:1137
                                OO00O0OO0OO0O0OOO ,O0O0OO0O0O0OO0OOO =OOOO0OOOOOO00000O ._verifynewact4ft (_O00O0O0000O000OOO )#line:1138
                            elif OOOO0OOOOOO00000O .proc =='Act4ftMiner':#line:1139
                                OO00O0OO0OO0O0OOO ,O0O0OO0O0O0OO0OOO =OOOO0OOOOOO00000O ._verifyact4ft (_O00O0O0000O000OOO )#line:1140
                            else :#line:1141
                                print ("Unsupported procedure : "+OOOO0OOOOOO00000O .proc )#line:1142
                                exit (0 )#line:1143
                            if OO00O0OO0OO0O0OOO ==True :#line:1144
                                OOO0000OO0OOOO0OO ={}#line:1145
                                OOO0000OO0OOOO0OO ["rule_id"]=OOOO0OOOOOO00000O .stats ['total_valid']#line:1146
                                OOO0000OO0OOOO0OO ["cedents_str"]={}#line:1147
                                OOO0000OO0OOOO0OO ["cedents_struct"]={}#line:1148
                                OOO0000OO0OOOO0OO ['traces']={}#line:1149
                                OOO0000OO0OOOO0OO ['trace_cedent_taskorder']={}#line:1150
                                OOO0000OO0OOOO0OO ['trace_cedent_dataorder']={}#line:1151
                                for OOO0O000OOOO0O0OO in OO00O00OOOOO0O000 ['cedents']:#line:1152
                                    OOO0000OO0OOOO0OO ['cedents_str'][OOO0O000OOOO0O0OO ['cedent_type']]=OOO0O000OOOO0O0OO ['generated_string']#line:1154
                                    OOO0000OO0OOOO0OO ['cedents_struct'][OOO0O000OOOO0O0OO ['cedent_type']]=OOO0O000OOOO0O0OO ['rule']#line:1155
                                    OOO0000OO0OOOO0OO ['traces'][OOO0O000OOOO0O0OO ['cedent_type']]=OOO0O000OOOO0O0OO ['traces']#line:1156
                                    OOO0000OO0OOOO0OO ['trace_cedent_taskorder'][OOO0O000OOOO0O0OO ['cedent_type']]=OOO0O000OOOO0O0OO ['trace_cedent']#line:1157
                                    OOO0000OO0OOOO0OO ['trace_cedent_dataorder'][OOO0O000OOOO0O0OO ['cedent_type']]=OOO0O000OOOO0O0OO ['trace_cedent_asindata']#line:1158
                                OOO0000OO0OOOO0OO ["params"]=O0O0OO0O0O0OO0OOO #line:1160
                                OOOO0OOOOOO00000O ._print_rule (OOO0000OO0OOOO0OO )#line:1162
                                OOOO0OOOOOO00000O .rulelist .append (OOO0000OO0OOOO0OO )#line:1168
                            OOOO0OOOOOO00000O .stats ['total_cnt']+=1 #line:1170
                            OOOO0OOOOOO00000O .stats ['total_ver']+=1 #line:1171
                    if _OO0OOOOOOOOO00OOO >=0 :#line:1172
                        if len (OO00O00OOOOO0O000 ['cedents_to_do'])>len (OO00O00OOOOO0O000 ['cedents']):#line:1173
                            OOOO0OOOOOO00000O ._start_cedent (OO00O00OOOOO0O000 )#line:1174
                    OO00O00OOOOO0O000 ['cedents'].pop ()#line:1175
                    if (len (_O00OOO0000000OO0O )<_OOOOOO000O0OO00O0 ):#line:1176
                        OOOO0OOOOOO00000O ._genvar (OO00O00OOOOO0O000 ,OOO000OOOO0O00OO0 ,_O00OOO0000000OO0O ,_OOO00O0OOO00000OO ,_O0000O0OOO000OOO0 ,_OOO00O0O0O0O00OO0 ,_OOOOOO000O0OO00O0 )#line:1177
                else :#line:1178
                    OO00O00OOOOO0O000 ['cedents'].pop ()#line:1179
                if len (_OO000000OO00O00O0 )<_O0OOOOOO00O0000O0 :#line:1180
                    OOOO0OOOOOO00000O ._gencomb (OO00O00OOOOO0O000 ,OOO000OOOO0O00OO0 ,_O00OOO0000000OO0O ,_OOO00O0OOO00000OO ,_OO000000OO00O00O0 ,_OOO0OO00OOO00OOOO ,_O00O0O0000O000OOO ,O0OO0O0O0OOOO00OO ,_OO0O0O00OO0000000 ,_OOO00O0O0O0O00OO0 ,_OOOOOO000O0OO00O0 ,_OO0O00O000OO0OOO0 ,_O0OOOOOO00O0000O0 )#line:1181
                _OO000000OO00O00O0 .pop ()#line:1182
    def _start_cedent (O0OOO0O0OO0000O00 ,O000O00O0OO0OOO00 ):#line:1184
        if len (O000O00O0OO0OOO00 ['cedents_to_do'])>len (O000O00O0OO0OOO00 ['cedents']):#line:1185
            _OO0O00OOOO0OO0OOO =[]#line:1186
            _OOOO0O0O0000O0OOO =[]#line:1187
            O000O0O00OO0O0000 ={}#line:1188
            O000O0O00OO0O0000 ['cedent_type']=O000O00O0OO0OOO00 ['cedents_to_do'][len (O000O00O0OO0OOO00 ['cedents'])]#line:1189
            O0OOO0O00O0OOO0OO =O000O0O00OO0O0000 ['cedent_type']#line:1190
            if ((O0OOO0O00O0OOO0OO [-1 ]=='-')|(O0OOO0O00O0OOO0OO [-1 ]=='+')):#line:1191
                O0OOO0O00O0OOO0OO =O0OOO0O00O0OOO0OO [:-1 ]#line:1192
            O000O0O00OO0O0000 ['defi']=O0OOO0O0OO0000O00 .kwargs .get (O0OOO0O00O0OOO0OO )#line:1194
            if (O000O0O00OO0O0000 ['defi']==None ):#line:1195
                print ("Error getting cedent ",O000O0O00OO0O0000 ['cedent_type'])#line:1196
            _O000OO0O0000OOO00 =int (0 )#line:1197
            O000O0O00OO0O0000 ['num_cedent']=len (O000O0O00OO0O0000 ['defi'].get ('attributes'))#line:1202
            if (O000O0O00OO0O0000 ['defi'].get ('type')=='con'):#line:1203
                _O000OO0O0000OOO00 =(1 <<O0OOO0O0OO0000O00 .data ["rows_count"])-1 #line:1204
            O0OOO0O0OO0000O00 ._genvar (O000O00O0OO0OOO00 ,O000O0O00OO0O0000 ,_OO0O00OOOO0OO0OOO ,_OOOO0O0O0000O0OOO ,_O000OO0O0000OOO00 ,O000O0O00OO0O0000 ['defi'].get ('minlen'),O000O0O00OO0O0000 ['defi'].get ('maxlen'))#line:1205
    def _calc_all (OOOO00OO0OOO00OO0 ,**OOO0O0OO00O0000OO ):#line:1208
        if "df"in OOO0O0OO00O0000OO :#line:1209
            OOOO00OO0OOO00OO0 ._prep_data (OOOO00OO0OOO00OO0 .kwargs .get ("df"))#line:1210
        if not (OOOO00OO0OOO00OO0 ._initialized ):#line:1211
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1212
        else :#line:1213
            OOOO00OO0OOO00OO0 ._calculate (**OOO0O0OO00O0000OO )#line:1214
    def _check_cedents (O0OOOO00OOO0O00O0 ,O000O0O00000O0OOO ,**O0000OOOOO0OO000O ):#line:1216
        O0OOOOOO0OOOOOOO0 =True #line:1217
        if (O0000OOOOO0OO000O .get ('quantifiers',None )==None ):#line:1218
            print (f"Error: missing quantifiers.")#line:1219
            O0OOOOOO0OOOOOOO0 =False #line:1220
            return O0OOOOOO0OOOOOOO0 #line:1221
        if (type (O0000OOOOO0OO000O .get ('quantifiers'))!=dict ):#line:1222
            print (f"Error: quantifiers are not dictionary type.")#line:1223
            O0OOOOOO0OOOOOOO0 =False #line:1224
            return O0OOOOOO0OOOOOOO0 #line:1225
        for O0OOOOO000OO0O00O in O000O0O00000O0OOO :#line:1227
            if (O0000OOOOO0OO000O .get (O0OOOOO000OO0O00O ,None )==None ):#line:1228
                print (f"Error: cedent {O0OOOOO000OO0O00O} is missing in parameters.")#line:1229
                O0OOOOOO0OOOOOOO0 =False #line:1230
                return O0OOOOOO0OOOOOOO0 #line:1231
            OO00OO0OOO00OO000 =O0000OOOOO0OO000O .get (O0OOOOO000OO0O00O )#line:1232
            if (OO00OO0OOO00OO000 .get ('minlen'),None )==None :#line:1233
                print (f"Error: cedent {O0OOOOO000OO0O00O} has no minimal length specified.")#line:1234
                O0OOOOOO0OOOOOOO0 =False #line:1235
                return O0OOOOOO0OOOOOOO0 #line:1236
            if not (type (OO00OO0OOO00OO000 .get ('minlen'))is int ):#line:1237
                print (f"Error: cedent {O0OOOOO000OO0O00O} has invalid type of minimal length ({type(OO00OO0OOO00OO000.get('minlen'))}).")#line:1238
                O0OOOOOO0OOOOOOO0 =False #line:1239
                return O0OOOOOO0OOOOOOO0 #line:1240
            if (OO00OO0OOO00OO000 .get ('maxlen'),None )==None :#line:1241
                print (f"Error: cedent {O0OOOOO000OO0O00O} has no maximal length specified.")#line:1242
                O0OOOOOO0OOOOOOO0 =False #line:1243
                return O0OOOOOO0OOOOOOO0 #line:1244
            if not (type (OO00OO0OOO00OO000 .get ('maxlen'))is int ):#line:1245
                print (f"Error: cedent {O0OOOOO000OO0O00O} has invalid type of maximal length.")#line:1246
                O0OOOOOO0OOOOOOO0 =False #line:1247
                return O0OOOOOO0OOOOOOO0 #line:1248
            if (OO00OO0OOO00OO000 .get ('type'),None )==None :#line:1249
                print (f"Error: cedent {O0OOOOO000OO0O00O} has no type specified.")#line:1250
                O0OOOOOO0OOOOOOO0 =False #line:1251
                return O0OOOOOO0OOOOOOO0 #line:1252
            if not ((OO00OO0OOO00OO000 .get ('type'))in (['con','dis'])):#line:1253
                print (f"Error: cedent {O0OOOOO000OO0O00O} has invalid type. Allowed values are 'con' and 'dis'.")#line:1254
                O0OOOOOO0OOOOOOO0 =False #line:1255
                return O0OOOOOO0OOOOOOO0 #line:1256
            if (OO00OO0OOO00OO000 .get ('attributes'),None )==None :#line:1257
                print (f"Error: cedent {O0OOOOO000OO0O00O} has no attributes specified.")#line:1258
                O0OOOOOO0OOOOOOO0 =False #line:1259
                return O0OOOOOO0OOOOOOO0 #line:1260
            for O00OO0OO0O0O0O0OO in OO00OO0OOO00OO000 .get ('attributes'):#line:1261
                if (O00OO0OO0O0O0O0OO .get ('name'),None )==None :#line:1262
                    print (f"Error: cedent {O0OOOOO000OO0O00O} / attribute {O00OO0OO0O0O0O0OO} has no 'name' attribute specified.")#line:1263
                    O0OOOOOO0OOOOOOO0 =False #line:1264
                    return O0OOOOOO0OOOOOOO0 #line:1265
                if not ((O00OO0OO0O0O0O0OO .get ('name'))in O0OOOO00OOO0O00O0 .data ["varname"]):#line:1266
                    print (f"Error: cedent {O0OOOOO000OO0O00O} / attribute {O00OO0OO0O0O0O0OO.get('name')} not in variable list. Please check spelling.")#line:1267
                    O0OOOOOO0OOOOOOO0 =False #line:1268
                    return O0OOOOOO0OOOOOOO0 #line:1269
                if (O00OO0OO0O0O0O0OO .get ('type'),None )==None :#line:1270
                    print (f"Error: cedent {O0OOOOO000OO0O00O} / attribute {O00OO0OO0O0O0O0OO.get('name')} has no 'type' attribute specified.")#line:1271
                    O0OOOOOO0OOOOOOO0 =False #line:1272
                    return O0OOOOOO0OOOOOOO0 #line:1273
                if not ((O00OO0OO0O0O0O0OO .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:1274
                    print (f"Error: cedent {O0OOOOO000OO0O00O} / attribute {O00OO0OO0O0O0O0OO.get('name')} has unsupported type {O00OO0OO0O0O0O0OO.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:1275
                    O0OOOOOO0OOOOOOO0 =False #line:1276
                    return O0OOOOOO0OOOOOOO0 #line:1277
                if (O00OO0OO0O0O0O0OO .get ('minlen'),None )==None :#line:1278
                    print (f"Error: cedent {O0OOOOO000OO0O00O} / attribute {O00OO0OO0O0O0O0OO.get('name')} has no minimal length specified.")#line:1279
                    O0OOOOOO0OOOOOOO0 =False #line:1280
                    return O0OOOOOO0OOOOOOO0 #line:1281
                if not (type (O00OO0OO0O0O0O0OO .get ('minlen'))is int ):#line:1282
                    if not (O00OO0OO0O0O0O0OO .get ('type')=='one'):#line:1283
                        print (f"Error: cedent {O0OOOOO000OO0O00O} / attribute {O00OO0OO0O0O0O0OO.get('name')} has invalid type of minimal length.")#line:1284
                        O0OOOOOO0OOOOOOO0 =False #line:1285
                        return O0OOOOOO0OOOOOOO0 #line:1286
                if (O00OO0OO0O0O0O0OO .get ('maxlen'),None )==None :#line:1287
                    print (f"Error: cedent {O0OOOOO000OO0O00O} / attribute {O00OO0OO0O0O0O0OO.get('name')} has no maximal length specified.")#line:1288
                    O0OOOOOO0OOOOOOO0 =False #line:1289
                    return O0OOOOOO0OOOOOOO0 #line:1290
                if not (type (O00OO0OO0O0O0O0OO .get ('maxlen'))is int ):#line:1291
                    if not (O00OO0OO0O0O0O0OO .get ('type')=='one'):#line:1292
                        print (f"Error: cedent {O0OOOOO000OO0O00O} / attribute {O00OO0OO0O0O0O0OO.get('name')} has invalid type of maximal length.")#line:1293
                        O0OOOOOO0OOOOOOO0 =False #line:1294
                        return O0OOOOOO0OOOOOOO0 #line:1295
        return O0OOOOOO0OOOOOOO0 #line:1296
    def _calculate (OOO0O00000OOOO00O ,**OO0O00OOOO0OO00O0 ):#line:1298
        if OOO0O00000OOOO00O .data ["data_prepared"]==0 :#line:1299
            print ("Error: data not prepared")#line:1300
            return #line:1301
        OOO0O00000OOOO00O .kwargs =OO0O00OOOO0OO00O0 #line:1302
        OOO0O00000OOOO00O .proc =OO0O00OOOO0OO00O0 .get ('proc')#line:1303
        OOO0O00000OOOO00O .quantifiers =OO0O00OOOO0OO00O0 .get ('quantifiers')#line:1304
        OOO0O00000OOOO00O ._init_task ()#line:1306
        OOO0O00000OOOO00O .stats ['start_proc_time']=time .time ()#line:1307
        OOO0O00000OOOO00O .task_actinfo ['cedents_to_do']=[]#line:1308
        OOO0O00000OOOO00O .task_actinfo ['cedents']=[]#line:1309
        if OO0O00OOOO0OO00O0 .get ("proc")=='UICMiner':#line:1312
            if not (OOO0O00000OOOO00O ._check_cedents (['ante'],**OO0O00OOOO0OO00O0 )):#line:1313
                return #line:1314
            _O0OO000000OO000OO =OO0O00OOOO0OO00O0 .get ("cond")#line:1316
            if _O0OO000000OO000OO !=None :#line:1317
                OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('cond')#line:1318
            else :#line:1319
                OO0O00OOO0000000O =OOO0O00000OOOO00O .cedent #line:1320
                OO0O00OOO0000000O ['cedent_type']='cond'#line:1321
                OO0O00OOO0000000O ['filter_value']=(1 <<OOO0O00000OOOO00O .data ["rows_count"])-1 #line:1322
                OO0O00OOO0000000O ['generated_string']='---'#line:1323
                OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('cond')#line:1325
                OOO0O00000OOOO00O .task_actinfo ['cedents'].append (OO0O00OOO0000000O )#line:1326
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('ante')#line:1327
            if OO0O00OOOO0OO00O0 .get ('target',None )==None :#line:1328
                print ("ERROR: no succedent/target variable defined for UIC Miner")#line:1329
                return #line:1330
            if not (OO0O00OOOO0OO00O0 .get ('target')in OOO0O00000OOOO00O .data ["varname"]):#line:1331
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1332
                return #line:1333
            if ("aad_score"in OOO0O00000OOOO00O .quantifiers ):#line:1334
                if not ("aad_weights"in OOO0O00000OOOO00O .quantifiers ):#line:1335
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1336
                    return #line:1337
                if not (len (OOO0O00000OOOO00O .quantifiers .get ("aad_weights"))==len (OOO0O00000OOOO00O .data ["dm"][OOO0O00000OOOO00O .data ["varname"].index (OOO0O00000OOOO00O .kwargs .get ('target'))])):#line:1338
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1339
                    return #line:1340
        elif OO0O00OOOO0OO00O0 .get ("proc")=='CFMiner':#line:1341
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do']=['cond']#line:1342
            if OO0O00OOOO0OO00O0 .get ('target',None )==None :#line:1343
                print ("ERROR: no target variable defined for CF Miner")#line:1344
                return #line:1345
            if not (OOO0O00000OOOO00O ._check_cedents (['cond'],**OO0O00OOOO0OO00O0 )):#line:1346
                return #line:1347
            if not (OO0O00OOOO0OO00O0 .get ('target')in OOO0O00000OOOO00O .data ["varname"]):#line:1348
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1349
                return #line:1350
            if ("aad"in OOO0O00000OOOO00O .quantifiers ):#line:1351
                if not ("aad_weights"in OOO0O00000OOOO00O .quantifiers ):#line:1352
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1353
                    return #line:1354
                if not (len (OOO0O00000OOOO00O .quantifiers .get ("aad_weights"))==len (OOO0O00000OOOO00O .data ["dm"][OOO0O00000OOOO00O .data ["varname"].index (OOO0O00000OOOO00O .kwargs .get ('target'))])):#line:1355
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1356
                    return #line:1357
        elif OO0O00OOOO0OO00O0 .get ("proc")=='4ftMiner':#line:1360
            if not (OOO0O00000OOOO00O ._check_cedents (['ante','succ'],**OO0O00OOOO0OO00O0 )):#line:1361
                return #line:1362
            _O0OO000000OO000OO =OO0O00OOOO0OO00O0 .get ("cond")#line:1364
            if _O0OO000000OO000OO !=None :#line:1365
                OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('cond')#line:1366
            else :#line:1367
                OO0O00OOO0000000O =OOO0O00000OOOO00O .cedent #line:1368
                OO0O00OOO0000000O ['cedent_type']='cond'#line:1369
                OO0O00OOO0000000O ['filter_value']=(1 <<OOO0O00000OOOO00O .data ["rows_count"])-1 #line:1370
                OO0O00OOO0000000O ['generated_string']='---'#line:1371
                OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('cond')#line:1373
                OOO0O00000OOOO00O .task_actinfo ['cedents'].append (OO0O00OOO0000000O )#line:1374
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('ante')#line:1378
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('succ')#line:1379
        elif OO0O00OOOO0OO00O0 .get ("proc")=='NewAct4ftMiner':#line:1380
            _O0OO000000OO000OO =OO0O00OOOO0OO00O0 .get ("cond")#line:1383
            if _O0OO000000OO000OO !=None :#line:1384
                OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('cond')#line:1385
            else :#line:1386
                OO0O00OOO0000000O =OOO0O00000OOOO00O .cedent #line:1387
                OO0O00OOO0000000O ['cedent_type']='cond'#line:1388
                OO0O00OOO0000000O ['filter_value']=(1 <<OOO0O00000OOOO00O .data ["rows_count"])-1 #line:1389
                OO0O00OOO0000000O ['generated_string']='---'#line:1390
                print (OO0O00OOO0000000O ['filter_value'])#line:1391
                OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('cond')#line:1392
                OOO0O00000OOOO00O .task_actinfo ['cedents'].append (OO0O00OOO0000000O )#line:1393
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('antv')#line:1394
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('sucv')#line:1395
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('ante')#line:1396
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('succ')#line:1397
        elif OO0O00OOOO0OO00O0 .get ("proc")=='Act4ftMiner':#line:1398
            _O0OO000000OO000OO =OO0O00OOOO0OO00O0 .get ("cond")#line:1401
            if _O0OO000000OO000OO !=None :#line:1402
                OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('cond')#line:1403
            else :#line:1404
                OO0O00OOO0000000O =OOO0O00000OOOO00O .cedent #line:1405
                OO0O00OOO0000000O ['cedent_type']='cond'#line:1406
                OO0O00OOO0000000O ['filter_value']=(1 <<OOO0O00000OOOO00O .data ["rows_count"])-1 #line:1407
                OO0O00OOO0000000O ['generated_string']='---'#line:1408
                print (OO0O00OOO0000000O ['filter_value'])#line:1409
                OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('cond')#line:1410
                OOO0O00000OOOO00O .task_actinfo ['cedents'].append (OO0O00OOO0000000O )#line:1411
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('antv-')#line:1412
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('antv+')#line:1413
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1414
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1415
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('ante')#line:1416
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('succ')#line:1417
        elif OO0O00OOOO0OO00O0 .get ("proc")=='SD4ftMiner':#line:1418
            if not (OOO0O00000OOOO00O ._check_cedents (['ante','succ','frst','scnd'],**OO0O00OOOO0OO00O0 )):#line:1421
                return #line:1422
            _O0OO000000OO000OO =OO0O00OOOO0OO00O0 .get ("cond")#line:1423
            if _O0OO000000OO000OO !=None :#line:1424
                OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('cond')#line:1425
            else :#line:1426
                OO0O00OOO0000000O =OOO0O00000OOOO00O .cedent #line:1427
                OO0O00OOO0000000O ['cedent_type']='cond'#line:1428
                OO0O00OOO0000000O ['filter_value']=(1 <<OOO0O00000OOOO00O .data ["rows_count"])-1 #line:1429
                OO0O00OOO0000000O ['generated_string']='---'#line:1430
                OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('cond')#line:1432
                OOO0O00000OOOO00O .task_actinfo ['cedents'].append (OO0O00OOO0000000O )#line:1433
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('frst')#line:1434
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('scnd')#line:1435
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('ante')#line:1436
            OOO0O00000OOOO00O .task_actinfo ['cedents_to_do'].append ('succ')#line:1437
        else :#line:1438
            print ("Unsupported procedure")#line:1439
            return #line:1440
        print ("Will go for ",OO0O00OOOO0OO00O0 .get ("proc"))#line:1441
        OOO0O00000OOOO00O .task_actinfo ['optim']={}#line:1444
        OO0O00OO00000OO0O =True #line:1445
        for O0O0OO00OOO0O0OO0 in OOO0O00000OOOO00O .task_actinfo ['cedents_to_do']:#line:1446
            try :#line:1447
                O0OOOOO00OOOOO0O0 =OOO0O00000OOOO00O .kwargs .get (O0O0OO00OOO0O0OO0 )#line:1448
                if O0OOOOO00OOOOO0O0 .get ('type')!='con':#line:1452
                    OO0O00OO00000OO0O =False #line:1453
            except :#line:1455
                O0OOOO0OO0O000000 =1 <2 #line:1456
        if OOO0O00000OOOO00O .options ['optimizations']==False :#line:1458
            OO0O00OO00000OO0O =False #line:1459
        OO0O0O00O0O0O0000 ={}#line:1460
        OO0O0O00O0O0O0000 ['only_con']=OO0O00OO00000OO0O #line:1461
        OOO0O00000OOOO00O .task_actinfo ['optim']=OO0O0O00O0O0O0000 #line:1462
        print ("Starting to mine rules.")#line:1470
        OOO0O00000OOOO00O ._start_cedent (OOO0O00000OOOO00O .task_actinfo )#line:1471
        OOO0O00000OOOO00O .stats ['end_proc_time']=time .time ()#line:1473
        print ("Done. Total verifications : "+str (OOO0O00000OOOO00O .stats ['total_cnt'])+", rules "+str (OOO0O00000OOOO00O .stats ['total_valid'])+", times: prep "+"{:.2f}".format (OOO0O00000OOOO00O .stats ['end_prep_time']-OOO0O00000OOOO00O .stats ['start_prep_time'])+"sec, processing "+"{:.2f}".format (OOO0O00000OOOO00O .stats ['end_proc_time']-OOO0O00000OOOO00O .stats ['start_proc_time'])+"sec")#line:1477
        O000OO00O0O00O000 ={}#line:1478
        O0O00OOOO0O0OOOO0 ={}#line:1479
        O0O00OOOO0O0OOOO0 ["task_type"]=OO0O00OOOO0OO00O0 .get ('proc')#line:1480
        O0O00OOOO0O0OOOO0 ["target"]=OO0O00OOOO0OO00O0 .get ('target')#line:1482
        O0O00OOOO0O0OOOO0 ["self.quantifiers"]=OOO0O00000OOOO00O .quantifiers #line:1483
        if OO0O00OOOO0OO00O0 .get ('cond')!=None :#line:1485
            O0O00OOOO0O0OOOO0 ['cond']=OO0O00OOOO0OO00O0 .get ('cond')#line:1486
        if OO0O00OOOO0OO00O0 .get ('ante')!=None :#line:1487
            O0O00OOOO0O0OOOO0 ['ante']=OO0O00OOOO0OO00O0 .get ('ante')#line:1488
        if OO0O00OOOO0OO00O0 .get ('succ')!=None :#line:1489
            O0O00OOOO0O0OOOO0 ['succ']=OO0O00OOOO0OO00O0 .get ('succ')#line:1490
        if OO0O00OOOO0OO00O0 .get ('opts')!=None :#line:1491
            O0O00OOOO0O0OOOO0 ['opts']=OO0O00OOOO0OO00O0 .get ('opts')#line:1492
        O000OO00O0O00O000 ["taskinfo"]=O0O00OOOO0O0OOOO0 #line:1493
        OOOOO0O0OOOOOO0O0 ={}#line:1494
        OOOOO0O0OOOOOO0O0 ["total_verifications"]=OOO0O00000OOOO00O .stats ['total_cnt']#line:1495
        OOOOO0O0OOOOOO0O0 ["valid_rules"]=OOO0O00000OOOO00O .stats ['total_valid']#line:1496
        OOOOO0O0OOOOOO0O0 ["total_verifications_with_opt"]=OOO0O00000OOOO00O .stats ['total_ver']#line:1497
        OOOOO0O0OOOOOO0O0 ["time_prep"]=OOO0O00000OOOO00O .stats ['end_prep_time']-OOO0O00000OOOO00O .stats ['start_prep_time']#line:1498
        OOOOO0O0OOOOOO0O0 ["time_processing"]=OOO0O00000OOOO00O .stats ['end_proc_time']-OOO0O00000OOOO00O .stats ['start_proc_time']#line:1499
        OOOOO0O0OOOOOO0O0 ["time_total"]=OOO0O00000OOOO00O .stats ['end_prep_time']-OOO0O00000OOOO00O .stats ['start_prep_time']+OOO0O00000OOOO00O .stats ['end_proc_time']-OOO0O00000OOOO00O .stats ['start_proc_time']#line:1500
        O000OO00O0O00O000 ["summary_statistics"]=OOOOO0O0OOOOOO0O0 #line:1501
        O000OO00O0O00O000 ["rules"]=OOO0O00000OOOO00O .rulelist #line:1502
        OOOOO0O0O0OO00O00 ={}#line:1503
        OOOOO0O0O0OO00O00 ["varname"]=OOO0O00000OOOO00O .data ["varname"]#line:1504
        OOOOO0O0O0OO00O00 ["catnames"]=OOO0O00000OOOO00O .data ["catnames"]#line:1505
        O000OO00O0O00O000 ["datalabels"]=OOOOO0O0O0OO00O00 #line:1506
        OOO0O00000OOOO00O .result =O000OO00O0O00O000 #line:1509
    def print_summary (OOO000OO0OO000O00 ):#line:1511
        print ("")#line:1512
        print ("CleverMiner task processing summary:")#line:1513
        print ("")#line:1514
        print (f"Task type : {OOO000OO0OO000O00.result['taskinfo']['task_type']}")#line:1515
        print (f"Number of verifications : {OOO000OO0OO000O00.result['summary_statistics']['total_verifications']}")#line:1516
        print (f"Number of rules : {OOO000OO0OO000O00.result['summary_statistics']['valid_rules']}")#line:1517
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(OOO000OO0OO000O00.result['summary_statistics']['time_total']))}")#line:1518
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(OOO000OO0OO000O00.result['summary_statistics']['time_prep']))}")#line:1520
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(OOO000OO0OO000O00.result['summary_statistics']['time_processing']))}")#line:1521
        print ("")#line:1522
    def print_hypolist (OOO000O0OOO0OO00O ):#line:1524
        OOO000O0OOO0OO00O .print_rulelist ();#line:1525
    def print_rulelist (OO0OO0OO00O0OOOOO ,sortby =None ,storesorted =False ):#line:1527
        def OO0O0O0OO00O0O000 (O0OO0OOOOOO0O0O00 ):#line:1528
            OOO00O0O0OOO0O0O0 =O0OO0OOOOOO0O0O00 ["params"]#line:1529
            return OOO00O0O0OOO0O0O0 .get (sortby ,0 )#line:1530
        print ("")#line:1532
        print ("List of rules:")#line:1533
        if OO0OO0OO00O0OOOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:1534
            print ("RULEID BASE  CONF  AAD    Rule")#line:1535
        elif OO0OO0OO00O0OOOOO .result ['taskinfo']['task_type']=="UICMiner":#line:1536
            print ("RULEID BASE  AAD_SCORE  Rule")#line:1537
        elif OO0OO0OO00O0OOOOO .result ['taskinfo']['task_type']=="CFMiner":#line:1538
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1539
        elif OO0OO0OO00O0OOOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1540
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1541
        else :#line:1542
            print ("Unsupported task type for rulelist")#line:1543
            return #line:1544
        O0O0O0O000OOOOO00 =OO0OO0OO00O0OOOOO .result ["rules"]#line:1545
        if sortby is not None :#line:1546
            O0O0O0O000OOOOO00 =sorted (O0O0O0O000OOOOO00 ,key =OO0O0O0OO00O0O000 ,reverse =True )#line:1547
            if storesorted :#line:1548
                OO0OO0OO00O0OOOOO .result ["rules"]=O0O0O0O000OOOOO00 #line:1549
        for O00OO00O0OO00O000 in O0O0O0O000OOOOO00 :#line:1551
            OOOO00OO00OOO0000 ="{:6d}".format (O00OO00O0OO00O000 ["rule_id"])#line:1552
            if OO0OO0OO00O0OOOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:1553
                OOOO00OO00OOO0000 =OOOO00OO00OOO0000 +" "+"{:5d}".format (O00OO00O0OO00O000 ["params"]["base"])+" "+"{:.3f}".format (O00OO00O0OO00O000 ["params"]["conf"])+" "+"{:+.3f}".format (O00OO00O0OO00O000 ["params"]["aad"])#line:1555
                OOOO00OO00OOO0000 =OOOO00OO00OOO0000 +" "+O00OO00O0OO00O000 ["cedents_str"]["ante"]+" => "+O00OO00O0OO00O000 ["cedents_str"]["succ"]+" | "+O00OO00O0OO00O000 ["cedents_str"]["cond"]#line:1556
            elif OO0OO0OO00O0OOOOO .result ['taskinfo']['task_type']=="UICMiner":#line:1557
                OOOO00OO00OOO0000 =OOOO00OO00OOO0000 +" "+"{:5d}".format (O00OO00O0OO00O000 ["params"]["base"])+" "+"{:.3f}".format (O00OO00O0OO00O000 ["params"]["aad_score"])#line:1558
                OOOO00OO00OOO0000 =OOOO00OO00OOO0000 +"     "+O00OO00O0OO00O000 ["cedents_str"]["ante"]+" => "+OO0OO0OO00O0OOOOO .result ['taskinfo']['target']+"(*) | "+O00OO00O0OO00O000 ["cedents_str"]["cond"]#line:1559
            elif OO0OO0OO00O0OOOOO .result ['taskinfo']['task_type']=="CFMiner":#line:1560
                OOOO00OO00OOO0000 =OOOO00OO00OOO0000 +" "+"{:5d}".format (O00OO00O0OO00O000 ["params"]["base"])+" "+"{:5d}".format (O00OO00O0OO00O000 ["params"]["s_up"])+" "+"{:5d}".format (O00OO00O0OO00O000 ["params"]["s_down"])#line:1561
                OOOO00OO00OOO0000 =OOOO00OO00OOO0000 +" "+O00OO00O0OO00O000 ["cedents_str"]["cond"]#line:1562
            elif OO0OO0OO00O0OOOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1563
                OOOO00OO00OOO0000 =OOOO00OO00OOO0000 +" "+"{:5d}".format (O00OO00O0OO00O000 ["params"]["base1"])+" "+"{:5d}".format (O00OO00O0OO00O000 ["params"]["base2"])+"    "+"{:.3f}".format (O00OO00O0OO00O000 ["params"]["ratioconf"])+"    "+"{:+.3f}".format (O00OO00O0OO00O000 ["params"]["deltaconf"])#line:1564
                OOOO00OO00OOO0000 =OOOO00OO00OOO0000 +"  "+O00OO00O0OO00O000 ["cedents_str"]["ante"]+" => "+O00OO00O0OO00O000 ["cedents_str"]["succ"]+" | "+O00OO00O0OO00O000 ["cedents_str"]["cond"]+" : "+O00OO00O0OO00O000 ["cedents_str"]["frst"]+" x "+O00OO00O0OO00O000 ["cedents_str"]["scnd"]#line:1565
            print (OOOO00OO00OOO0000 )#line:1567
        print ("")#line:1568
    def print_hypo (OOOOO0OOO0OO0O000 ,O000OOO00O0OO0O0O ):#line:1570
        OOOOO0OOO0OO0O000 .print_rule (O000OOO00O0OO0O0O )#line:1571
    def print_rule (O00O00OOOOOOO0O0O ,OOO0OOOO0OO00OOO0 ):#line:1574
        print ("")#line:1575
        if (OOO0OOOO0OO00OOO0 <=len (O00O00OOOOOOO0O0O .result ["rules"])):#line:1576
            if O00O00OOOOOOO0O0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1577
                print ("")#line:1578
                OOO00OOO0O00OOO0O =O00O00OOOOOOO0O0O .result ["rules"][OOO0OOOO0OO00OOO0 -1 ]#line:1579
                print (f"Rule id : {OOO00OOO0O00OOO0O['rule_id']}")#line:1580
                print ("")#line:1581
                print (f"Base : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['base'])}  Relative base : {'{:.3f}'.format(OOO00OOO0O00OOO0O['params']['rel_base'])}  CONF : {'{:.3f}'.format(OOO00OOO0O00OOO0O['params']['conf'])}  AAD : {'{:+.3f}'.format(OOO00OOO0O00OOO0O['params']['aad'])}  BAD : {'{:+.3f}'.format(OOO00OOO0O00OOO0O['params']['bad'])}")#line:1582
                print ("")#line:1583
                print ("Cedents:")#line:1584
                print (f"  antecedent : {OOO00OOO0O00OOO0O['cedents_str']['ante']}")#line:1585
                print (f"  succcedent : {OOO00OOO0O00OOO0O['cedents_str']['succ']}")#line:1586
                print (f"  condition  : {OOO00OOO0O00OOO0O['cedents_str']['cond']}")#line:1587
                print ("")#line:1588
                print ("Fourfold table")#line:1589
                print (f"    |  S  |  ¬S |")#line:1590
                print (f"----|-----|-----|")#line:1591
                print (f" A  |{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold'][0])}|{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold'][1])}|")#line:1592
                print (f"----|-----|-----|")#line:1593
                print (f"¬A  |{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold'][2])}|{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold'][3])}|")#line:1594
                print (f"----|-----|-----|")#line:1595
            elif O00O00OOOOOOO0O0O .result ['taskinfo']['task_type']=="CFMiner":#line:1596
                print ("")#line:1597
                OOO00OOO0O00OOO0O =O00O00OOOOOOO0O0O .result ["rules"][OOO0OOOO0OO00OOO0 -1 ]#line:1598
                print (f"Rule id : {OOO00OOO0O00OOO0O['rule_id']}")#line:1599
                print ("")#line:1600
                O0O0O00000OO00OO0 =""#line:1601
                if ('aad'in OOO00OOO0O00OOO0O ['params']):#line:1602
                    O0O0O00000OO00OO0 ="aad : "+str (OOO00OOO0O00OOO0O ['params']['aad'])#line:1603
                print (f"Base : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['base'])}  Relative base : {'{:.3f}'.format(OOO00OOO0O00OOO0O['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['max'])}  Histogram minimum : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(OOO00OOO0O00OOO0O['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(OOO00OOO0O00OOO0O['params']['rel_min'])} {O0O0O00000OO00OO0}")#line:1605
                print ("")#line:1606
                print (f"Condition  : {OOO00OOO0O00OOO0O['cedents_str']['cond']}")#line:1607
                print ("")#line:1608
                print (f"Histogram                      {OOO00OOO0O00OOO0O['params']['hist']}")#line:1609
                if ('aad'in OOO00OOO0O00OOO0O ['params']):#line:1610
                    print (f"Histogram on full set          {OOO00OOO0O00OOO0O['params']['hist_full']}")#line:1611
                    print (f"Relative histogram             {OOO00OOO0O00OOO0O['params']['rel_hist']}")#line:1612
                    print (f"Relative histogram on full set {OOO00OOO0O00OOO0O['params']['rel_hist_full']}")#line:1613
            elif O00O00OOOOOOO0O0O .result ['taskinfo']['task_type']=="UICMiner":#line:1614
                print ("")#line:1615
                OOO00OOO0O00OOO0O =O00O00OOOOOOO0O0O .result ["rules"][OOO0OOOO0OO00OOO0 -1 ]#line:1616
                print (f"Rule id : {OOO00OOO0O00OOO0O['rule_id']}")#line:1617
                print ("")#line:1618
                O0O0O00000OO00OO0 =""#line:1619
                if ('aad_score'in OOO00OOO0O00OOO0O ['params']):#line:1620
                    O0O0O00000OO00OO0 ="aad score : "+str (OOO00OOO0O00OOO0O ['params']['aad_score'])#line:1621
                print (f"Base : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['base'])}  Relative base : {'{:.3f}'.format(OOO00OOO0O00OOO0O['params']['rel_base'])}   {O0O0O00000OO00OO0}")#line:1623
                print ("")#line:1624
                print (f"Condition  : {OOO00OOO0O00OOO0O['cedents_str']['cond']}")#line:1625
                print (f"Antecedent : {OOO00OOO0O00OOO0O['cedents_str']['ante']}")#line:1626
                print ("")#line:1627
                print (f"Histogram                                        {OOO00OOO0O00OOO0O['params']['hist']}")#line:1628
                if ('aad_score'in OOO00OOO0O00OOO0O ['params']):#line:1629
                    print (f"Histogram on full set with condition             {OOO00OOO0O00OOO0O['params']['hist_cond']}")#line:1630
                    print (f"Relative histogram                               {OOO00OOO0O00OOO0O['params']['rel_hist']}")#line:1631
                    print (f"Relative histogram on full set with condition    {OOO00OOO0O00OOO0O['params']['rel_hist_cond']}")#line:1632
                O0O00O000O0O0O0O0 =O00O00OOOOOOO0O0O .result ['datalabels']['catnames'][O00O00OOOOOOO0O0O .result ['datalabels']['varname'].index (O00O00OOOOOOO0O0O .result ['taskinfo']['target'])]#line:1633
                print (" ")#line:1635
                print ("Interpretation:")#line:1636
                for OOOO00OOO0O00OO0O in range (len (O0O00O000O0O0O0O0 )):#line:1637
                  OO0OOOOO0000OO0O0 =0 #line:1638
                  if OOO00OOO0O00OOO0O ['params']['rel_hist'][OOOO00OOO0O00OO0O ]>0 :#line:1639
                      OO0OOOOO0000OO0O0 =OOO00OOO0O00OOO0O ['params']['rel_hist'][OOOO00OOO0O00OO0O ]/OOO00OOO0O00OOO0O ['params']['rel_hist_cond'][OOOO00OOO0O00OO0O ]#line:1640
                  OOO00OOO0OO0000O0 =''#line:1641
                  if not (OOO00OOO0O00OOO0O ['cedents_str']['cond']=='---'):#line:1642
                      OOO00OOO0OO0000O0 ="For "+OOO00OOO0O00OOO0O ['cedents_str']['cond']+": "#line:1643
                  print (f"    {OOO00OOO0OO0000O0}{O00O00OOOOOOO0O0O.result['taskinfo']['target']}({O0O00O000O0O0O0O0[OOOO00OOO0O00OO0O]}) has occurence {'{:.1%}'.format(OOO00OOO0O00OOO0O['params']['rel_hist_cond'][OOOO00OOO0O00OO0O])}, with antecedent it has occurence {'{:.1%}'.format(OOO00OOO0O00OOO0O['params']['rel_hist'][OOOO00OOO0O00OO0O])}, that is {'{:.3f}'.format(OO0OOOOO0000OO0O0)} times more.")#line:1645
            elif O00O00OOOOOOO0O0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1646
                print ("")#line:1647
                OOO00OOO0O00OOO0O =O00O00OOOOOOO0O0O .result ["rules"][OOO0OOOO0OO00OOO0 -1 ]#line:1648
                print (f"Rule id : {OOO00OOO0O00OOO0O['rule_id']}")#line:1649
                print ("")#line:1650
                print (f"Base1 : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['base1'])} Base2 : {'{:5d}'.format(OOO00OOO0O00OOO0O['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(OOO00OOO0O00OOO0O['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(OOO00OOO0O00OOO0O['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(OOO00OOO0O00OOO0O['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(OOO00OOO0O00OOO0O['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(OOO00OOO0O00OOO0O['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(OOO00OOO0O00OOO0O['params']['ratioconf'])}")#line:1651
                print ("")#line:1652
                print ("Cedents:")#line:1653
                print (f"  antecedent : {OOO00OOO0O00OOO0O['cedents_str']['ante']}")#line:1654
                print (f"  succcedent : {OOO00OOO0O00OOO0O['cedents_str']['succ']}")#line:1655
                print (f"  condition  : {OOO00OOO0O00OOO0O['cedents_str']['cond']}")#line:1656
                print (f"  first set  : {OOO00OOO0O00OOO0O['cedents_str']['frst']}")#line:1657
                print (f"  second set : {OOO00OOO0O00OOO0O['cedents_str']['scnd']}")#line:1658
                print ("")#line:1659
                print ("Fourfold tables:")#line:1660
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1661
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1662
                print (f" A  |{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold1'][0])}|{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold2'][0])}|{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold2'][1])}|")#line:1663
                print (f"----|-----|-----|  ----|-----|-----|")#line:1664
                print (f"¬A  |{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold1'][2])}|{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold2'][2])}|{'{:5d}'.format(OOO00OOO0O00OOO0O['params']['fourfold2'][3])}|")#line:1665
                print (f"----|-----|-----|  ----|-----|-----|")#line:1666
            else :#line:1667
                print ("Unsupported task type for rule details")#line:1668
            print ("")#line:1672
        else :#line:1673
            print ("No such rule.")#line:1674
    def get_rulecount (O0OO0O00O0O000OOO ):#line:1676
        return len (O0OO0O00O0O000OOO .result ["rules"])#line:1677
    def get_fourfold (O0O0OO00OO0O0OOO0 ,O00OOOO0OO0OO0000 ,order =0 ):#line:1679
        if (O00OOOO0OO0OO0000 <=len (O0O0OO00OO0O0OOO0 .result ["rules"])):#line:1681
            if O0O0OO00OO0O0OOO0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1682
                OOOOOO00OOOO00OO0 =O0O0OO00OO0O0OOO0 .result ["rules"][O00OOOO0OO0OO0000 -1 ]#line:1683
                return OOOOOO00OOOO00OO0 ['params']['fourfold']#line:1684
            elif O0O0OO00OO0O0OOO0 .result ['taskinfo']['task_type']=="CFMiner":#line:1685
                print ("Error: fourfold for CFMiner is not defined")#line:1686
                return None #line:1687
            elif O0O0OO00OO0O0OOO0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1688
                OOOOOO00OOOO00OO0 =O0O0OO00OO0O0OOO0 .result ["rules"][O00OOOO0OO0OO0000 -1 ]#line:1689
                if order ==1 :#line:1690
                    return OOOOOO00OOOO00OO0 ['params']['fourfold1']#line:1691
                if order ==2 :#line:1692
                    return OOOOOO00OOOO00OO0 ['params']['fourfold2']#line:1693
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:1694
                return None #line:1695
            else :#line:1696
                print ("Unsupported task type for rule details")#line:1697
        else :#line:1698
            print ("No such rule.")#line:1699
    def get_hist (OOOOOO0O00OOOOOOO ,O0000OO0O0OOOO0OO ):#line:1701
        if (O0000OO0O0OOOO0OO <=len (OOOOOO0O00OOOOOOO .result ["rules"])):#line:1703
            if OOOOOO0O00OOOOOOO .result ['taskinfo']['task_type']=="CFMiner":#line:1704
                O00O0OO000O000OOO =OOOOOO0O00OOOOOOO .result ["rules"][O0000OO0O0OOOO0OO -1 ]#line:1705
                return O00O0OO000O000OOO ['params']['hist']#line:1706
            elif OOOOOO0O00OOOOOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1707
                print ("Error: SD4ft-Miner has no histogram")#line:1708
                return None #line:1709
            elif OOOOOO0O00OOOOOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:1710
                print ("Error: 4ft-Miner has no histogram")#line:1711
                return None #line:1712
            else :#line:1713
                print ("Unsupported task type for rule details")#line:1714
        else :#line:1715
            print ("No such rule.")#line:1716
    def get_hist_cond (O00O0000O00000O0O ,OOOO0O00OO0O00OOO ):#line:1719
        if (OOOO0O00OO0O00OOO <=len (O00O0000O00000O0O .result ["rules"])):#line:1721
            if O00O0000O00000O0O .result ['taskinfo']['task_type']=="UICMiner":#line:1722
                OOO00000OOOO0OOO0 =O00O0000O00000O0O .result ["rules"][OOOO0O00OO0O00OOO -1 ]#line:1723
                return OOO00000OOOO0OOO0 ['params']['hist_cond']#line:1724
            elif O00O0000O00000O0O .result ['taskinfo']['task_type']=="CFMiner":#line:1725
                OOO00000OOOO0OOO0 =O00O0000O00000O0O .result ["rules"][OOOO0O00OO0O00OOO -1 ]#line:1726
                return OOO00000OOOO0OOO0 ['params']['hist']#line:1727
            elif O00O0000O00000O0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1728
                print ("Error: SD4ft-Miner has no histogram")#line:1729
                return None #line:1730
            elif O00O0000O00000O0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1731
                print ("Error: 4ft-Miner has no histogram")#line:1732
                return None #line:1733
            else :#line:1734
                print ("Unsupported task type for rule details")#line:1735
        else :#line:1736
            print ("No such rule.")#line:1737
    def get_quantifiers (OOO0000O0000OOO0O ,OO0OO00OO0OO0000O ,order =0 ):#line:1739
        if (OO0OO00OO0OO0000O <=len (OOO0000O0000OOO0O .result ["rules"])):#line:1741
            O0000O0000OOO0000 =OOO0000O0000OOO0O .result ["rules"][OO0OO00OO0OO0000O -1 ]#line:1742
            if OOO0000O0000OOO0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1743
                return O0000O0000OOO0000 ['params']#line:1744
            elif OOO0000O0000OOO0O .result ['taskinfo']['task_type']=="CFMiner":#line:1745
                return O0000O0000OOO0000 ['params']#line:1746
            elif OOO0000O0000OOO0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1747
                return O0000O0000OOO0000 ['params']#line:1748
            else :#line:1749
                print ("Unsupported task type for rule details")#line:1750
        else :#line:1751
            print ("No such rule.")#line:1752
