function initialization() {
    let  tree_all = "<div class='tree_all' id ='tree_all_id'></div>";
    let  tree_view = "<div class= 'tree_view' id ='tree_view_id'></div>";
    let  tree_header = "<div class='tree_header' id='tree_header_id'></div>";
    let  date_all = " <div class='date_all' id='date_all_id'></div>";
    let  date_header = "<div class ='date_header' id='date_header_id'></div>";
    let  date_view = "<div class='date_view' id='date_view_id'></div>";
    let  tree_header_name ="<div class = 'tree_header_name' id ='tree_header_name_id'>Name</div>";
    let  tree_header_days_and_add ="<div class='tree_header_days_and_add' id='tree_header_days_and_add_id'></div>";
    let  tree_header_days ="<div class = 'tree_header_days ' id ='tree_header_days_id'>Days</div>";
    let  tree_header_add_icon = "<div class = 'tree_header_add_icon tree_view_icon' id ='tree_header_add_icon_id'></div>";

    $("#TaskContainer").append(tree_all,date_all);
    $("#tree_all_id").append(tree_header,tree_view);
    $("#date_all_id").append(date_header,date_view);
    $("#tree_header_id").append(tree_header_name,tree_header_days_and_add);
    $("#tree_header_days_and_add_id").append(tree_header_days,tree_header_add_icon);
}
//开始结束日期
var task_date = {
    date_start_year: 2019,
    date_start_month: 1,// Date 类月份从0开始
    date_start_day: 1,
    date_end_year: 2019,
    date_end_month: 12,
    date_end_day: 31,
    start_date: "2019-1-1",
    end_date: "2019-12-31",
    get_days: function (cur_year,cur_month){
        let days = new Date(cur_year,cur_month,0);
        return days.getDate();
    },
    distance_days:function (start_date,end_date) {
        //计算日期之差
        var strSeparator = "-"; //日期分隔符
        var oDate1;
        var oDate2;
        var iDays;
        oDate1= start_date.split(strSeparator);
        oDate2= end_date.split(strSeparator);
        var strDateS = new Date(oDate1[0], oDate1[1]-1, oDate1[2]);
        var strDateE = new Date(oDate2[0], oDate2[1]-1, oDate2[2]);
        //把相差的毫秒数转换为天数
        iDays = parseInt(Math.abs(strDateS - strDateE ) / 1000 / 60 / 60 /24);
        return iDays ;
    }
};
var create_Main_task = {
    row_num  : 0, //第几行
    index : 0,   //第几个子任务
    task_name : null,
    hierarchies : 0, //父层次数
    parent_object :null,//自身元素id
    child_object : [],
    child_num: 0,
    item_id: [
        "tree_view_row_id",
        "tree_view_row_item_first_id",
        "tree_view_row_item_first_icon0_id",
        "tree_view_row_item_first_icon1_id",
        "tree_view_row_item_first_text_id",
        "tree_view_row_item_last_id",
        "tree_view_row_item_last_icon0_id",
        "tree_view_row_item_last_icon1_id",
        "tree_view_row_item_last_text_id"
    ]
};
function add_time_header(task_date){
    let year = task_date.date_start_year;
    let start_month = task_date.date_start_month;
    let end_month = task_date.date_end_month;
    let date_header_month_all = "<div id = 'date_header_month_all_id' class = 'date_header_month_all'></div>";
    let date_header_day_all = "<div id = 'date_header_day_all_id' class = 'date_header_day_all'></div>";
    $("#date_header_id").append(date_header_month_all,date_header_day_all);
    for (let num = start_month;num<=end_month;num++){
        let days = task_date.get_days(task_date.date_start_year,num,0);
        let date_header_month = "<div id='date_header_month_"+num+"' class = 'date_header_month'>"+year+"-"+num+"</div>";
        let date_header_month_days = "<div id='date_header_month_days_"+num+"' class='date_header_month_days'> </div>";
        $("#date_header_month_all_id").append(date_header_month);
        $("#date_header_day_all_id").append(date_header_month_days);

        let month_width = days*15;
        let month_days_width = days*15;
        $("#date_header_month_"+num).css("width",""+month_width+"px");
        let month_days = $("#date_header_month_days_"+num);
        month_days.css("width",+month_days_width+"px");
        for(let da = 1; da <= days; da++) {
            let date_header_day = "<div id ='date_header_month_days_" + num +"_" +da+ "' class='date_header_day'>" + da + "</div>";
            month_days.append(date_header_day);
        }
    }
}
//global process
var global = {
    row_count : 0,
    color :"null",
    task_name :"null",
    date : "null",
    div_status:false,
    task_object:create_Main_task,
};
function send_task() {
    $("#child_task_id").css("display","none");
    $("#fade").css("display","none");
    global.task_name = $("input[id ='child_task_name_id']").val();
    global.date = $("input[id ='task_date_id']").val();
    let that = global.task_object;//父对象
    let new_tree_row = new Add_child_task(that);
    // new_tree_row.slid_block();
    if (that!== create_Main_task) {
        that.child_object.push(new_tree_row);
        that.child_item.push(that.item_id[0]+"_"+that.child_num);
        new_tree_row.parent_object.alter_father_sliding_length();
       //入数组 列表上的兄弟
    }
    else{
        // console.log("Main_task");
        that.index++;
        that.row_num++;
    }
    that.child_num = that.child_num +1; //child_item中项数 第二项目始为其创建的节点
    global.task_object = create_Main_task;

}
function quit(){
    document.getElementById('child_task_id').style.display='none';
    document.getElementById('fade').style.display='none';
    $("#child_task_id").css("display","none");
    // document.getElementById('child_task_id').style.display='none';
}
$(function(){
    initialization();
    add_time_header(task_date);
    $( "#task_date_id" ).daterangepicker();

    $("#tree_header_add_icon_id").click(function () {
        document.getElementById('child_task_id').style.display='block';
        document.getElementById('fade').style.display='block';
        $("#task_need_time_id").hide();
        $("input[name='task_name'] ").val("");
    });
});