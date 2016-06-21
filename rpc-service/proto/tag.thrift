struct tagResult{
    1: list<string> pos_tag,
    2: list<string> neg_tag,
    3: map<string, string> polarity_res,
    4: map<string, double> range_res_lower,
    5: map<string, double> range_res_upper,
    6: map<string, string> kv_value,
    7: string mk_str;
}

struct basicStruct {
    1: map<string, string> bs,
}

service Tagger {
    map<string,string> basic_struct(1:string text),

    tagResult tag(1:string text, 2:string mode),

    map<string, string> test(1:map<string, string>param),
}
