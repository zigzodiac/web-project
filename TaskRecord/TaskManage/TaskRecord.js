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
        return iDays+1 ;
    }
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
            console.log(days);
        }
    }
}

//添加空白日期div
class Add_day {
    constructor(row){
        let year = task_date.date_start_year;
        let year_days = task_date.distance_days(task_date.start_date,task_date.end_date);
        let start_month = task_date.date_start_month;
        let end_month = task_date.date_end_month;
        //行div
        let date_view_row = "<div id = 'date_view_row_"+row+"' class = 'date_view_row'></div>";

        $("#date_view_id").append(date_view_row);
        let view_row = $("#date_view_row_"+row);
        view_row.css("width",year_days*15+"px");
        for (let num = start_month;num<=end_month;num++){
            let days = task_date.get_days(task_date.date_start_year,num,0);
            let date_view_row_month = "<div id='date_view_row_month_"+row+"_"+num+"' class = 'date_view_row_month'></div>";
            let month_width = days*15;
            view_row.append(date_view_row_month);
            let view_month = $("#date_view_row_month_"+row+"_"+num);
            view_month.css("width",month_width+"px");
            for(let da = 1; da <= days; da++) {
                let view_day = "<div id ='date_view_row_month_day_"+row+"_" + num +"_" +da+ "' class='date_view_row_month_day'></div>";
                view_month.append(view_day);
                console.log(row,num,da);
            }
        }
    }
}

class Add_task {
    constructor(index, task_name) {
        this.row_num = index;      //位置
        this.child_num = 0;        //子任务数
        this.task_name = task_name;//任务名称
        this.task_time = 1;   //完成任务时间
        this.hierarchies = 0; //层次数 以1起步
        this.item_id = ["tree_view_row_id_"+index,
            "tree_view_row_item_first_id_"+index,
            "tree_view_row_item_first_icon0_id_"+index,
            "tree_view_row_item_first_icon1_id_"+index,
            "tree_view_row_item_first_text_id_"+index,
            "tree_view_row_item_last_id_"+index,
            "tree_view_row_item_last_icon0_id_"+index,
            "tree_view_row_item_last_icon1_id_"+index,
            "tree_view_row_item_last_text_id_"+index];
        this.child_item =["tree_view_row_id_"+index];
        this.flag_change = true;//信号子任务隐藏否
        ////////////
        this.child_num =0;
        this.brother_object_id = null;//不需要
        this.child_object = [];
        this.row_div_id = this.item_id[0];//记录对象对应的div的id
        /////////////////
        this.date_brother_id = 0;
        this.date_id = "date_view_row_"+index;
        let that = this;
        this.div_left = 0;
        this.div_width = 0;
        this.parent_object = null;
        this.append_task = function(item_id){
            let tem_child_object = [];
            let tree_view_row ="<div class= 'tree_view_row'  id ='tree_view_row_id_"+index+"'></div>";
            //行开始部分
            let tree_view_row_item_first = "<div class= 'tree_view_row_item_first' id ='tree_view_row_item_first_id_"+index+"'></div>";
            let tree_view_row_item_first_icon0 = "<div class= 'tree_view_row_item_first_icon0 tree_file_subtract_icon tree_view_icon' id ='tree_view_row_item_first_icon0_id_"+index+"'></div>";
            let tree_view_row_item_first_icon1 = "<div class= 'tree_view_row_item_first_icon1 tree_file_merge_icon tree_view_icon' id ='tree_view_row_item_first_icon1_id_"+index+"'></div>";
            let tree_view_row_item_first_text = "<div class='tree_view_text' id='tree_view_row_item_first_text_id_"+index+"'>"+task_name+"</div>";
            //行结尾部分
            let tree_view_row_item_last = "<div class= 'tree_view_row_item_last' id ='tree_view_row_item_last_id_"+index+"'></div>";
            let tree_view_row_item_last_icon0 = "<div class= 'tree_view_row_item_last_icon0 tree_view_flag_icon tree_view_icon' id ='tree_view_row_item_last_icon0_id_"+index+"'></div>";
            let tree_view_row_item_last_icon1 = "<div class= 'tree_view_row_item_last_icon1 tree_plus_icon tree_view_icon' id ='tree_view_row_item_last_icon1_id_"+index+"'></div>";
            let tree_view_row_item_last_text = "<div class='tree_view_row_item_last_text' id='tree_view_row_item_last_text_id_"+index+"'>1</div>";
            $("#tree_view_id").append(tree_view_row);

            let tree_view_row_id = $("#tree_view_row_id_"+index);
            // tree_view_row_id.hover()
            console.log(tree_view_row);
            tree_view_row_id.append(tree_view_row_item_first, tree_view_row_item_last);
            $("#tree_view_row_item_first_id_"+index).append(tree_view_row_item_first_icon0, tree_view_row_item_first_icon1, tree_view_row_item_first_text);
            $("#tree_view_row_item_first_icon0_id_"+index).click(function() {
                // this.alter_text = $("#tree_view_row_item_first_text_id"+index);
                // $("#tree_view_row_item_first_text_id_"+index).text("zane");
                // console.log("#tree_view_row_item_first_text_id_"+index);
                if (that.child_object.length>0){
                    if (that.flag_change){//隐藏
                        for (let value of that.child_object){
                            value.child_hide();
                            tem_child_object.push(value);
                        }
                        that.flag_change = false;
                        let child_item = $("#"+that.item_id[2]);
                        child_item.removeClass("tree_file_plus_icon");
                        child_item.addClass("tree_file_subtract_icon");
                    }
                    else{//显示
                        for (let value of tem_child_object){
                            let row_id =  $("#"+value.row_div_id);
                            if(row_id.is(":hidden")) {
                                row_id.show();
                            }
                            let date_id = $("#"+value.date_id);
                            if (date_id.is(":hidden")){
                                date_id.show();
                            }
                        }
                        that.flag_change = true;
                        let child_item = $("#"+that.item_id[2]);
                        child_item.removeClass("tree_file_subtract_icon");
                        child_item.addClass("tree_file_plus_icon");
                    }

                }
            });
            $("#tree_view_row_item_last_id_"+index).append(tree_view_row_item_last_icon0, tree_view_row_item_last_text, tree_view_row_item_last_icon1);
            $("#tree_view_row_item_last_icon1_id_"+index).click(function() {
                $("#fade").css("display","block");
                $("#child_task_id").css("display","block");
                // alert(item_id[0]);
                global.task_object = that;
                let tem = 0;
                // while(global.div_status){
                //     tem++;
                // }
                // that.child_item.push(that.item_id[0]+"_"+that.child_num);
                // //初始化子任务对象
                // //that.row_num,that.child_num,that.hierarchies,"child",item_id,that.child_item[that.child_num],
                // let child_task = new Add_child_task(that);
                // child_task.append_task();//添加子任务
                // child_task.add_day();
                // child_task.mouse_incident();
                // that.child_object.push(child_task);
                // if (that.flag_change){
                //     let child_item = $("#"+that.item_id[2]);
                //     child_item.removeClass("tree_file_subtract_icon");
                //     child_item.addClass("tree_file_plus_icon");
                // }
                // that.child_num = that.child_num + 1;//计数
                // $("#tree_view_row_id_"+index).hide();
            });
        }
    }
    mouse_incident(){
        let current_id  = $("#"+this.row_div_id);
        let date_row_id = $("#"+this.date_id);
        current_id.hover(
            function () {
                current_id.css("background-color","#fafa25");
                date_row_id.css("background-color", "#fafa25");
            },
            function () {
                current_id.css("background-color","#838383");
                date_row_id.css("background-color", "#838383");
            }
        );
    }
    slid_block() {
        this.div_left = 0;
        this.div_width = 0;
        let sliding_block = "<div class='date_view_row_block' id ='" + this.date_id + "_block'></div>";
        let day_block_left = "<div class ='date_view_day_block_left' id='" + this.date_id + "_day_block_left'></div>";
        let day_block_right = "<div class ='date_view_day_block_right' id='" + this.date_id + "_day_block_right'></div>";
        $("#" + this.date_id).append(sliding_block);
        let row_block = $("#" + this.date_id + "_block");
        row_block.append(day_block_left, day_block_right);
        row_block.css("width", this.div_width + "px");
        row_block.css("left", this.div_left + "px");
        //绑定事件
        let day_block_left_hover = $("#" + this.date_id + "_day_block_left");
        let day_block_right_hover = $("#" + this.date_id + "_day_block_right");
        let add_width = 0;
        day_block_left_hover.hover(
            function () {
                day_block_left_hover.css("background","rgba(130,228,255,0.5)")
            },
            function () {
                day_block_left_hover.css("background","rgba(255, 232, 63, 0.5)")
            }
        );
        day_block_right_hover.hover(
            function () {
                day_block_right_hover.css("background","rgba(130,228,255,0.5)")
            },
            function () {
                day_block_right_hover.css("background","rgba(255, 232, 63, 0.5)")
            }
        );
        let move_width = 0;
        row_block.draggable({
            create: function (event, ui) {
            },
            drag: function (event, ui) {
                // day_block_left_hover.css("width","15px");
                // ui.position.left = Math.min( 100, ui.position.left );
                console.log("1111111", Math.round(ui.position.left / 15));
                // move_width=left_days*15-ui.position.left/15
                // row_block.css("left",ui.position.left+"px");
                // row_block.css("width",days*15-ui.position.left+"px");
            },
            axis: "x",
            grid: [15, 20],
            // minWidth : 15,
            containment:"parent",
        });
        row_block.resizable({
            create: function( event, ui ) {},
            containment: "parent",
            axis: "x",
            grid: 15,
            // handles:{'w':day_block_left_hover,
            //     "e":day_block_right_hover},
            handles:"w,e",
            resize: function (event, ui) {
                console.log("resize222222222222",Math.round(ui.position.left / 15));
                console.log("resize222222222222",ui.size.width);
            }
        });
    }
    alter_size(current_width,current_left){
        let block_size = $("#" + this.date_id + "_block");
        let cur_width = 0;
        let cur_left = 0;
        if (current_width<this.div_left){
            cur_left = current_left;
            block_size.css("width",cur_left+"px");

        }
        if(current_width+current_left>this.div_width+this.div_left){
            cur_width = current_width+current_left -this.div_width+this.div_left;
            cur_width=cur_width +this.div_width;
            block_size.css("left",cur_width+"px");
        }
        if(this.parent_object){
            this.parent_object.alter_size(cur_width,cur_left);
        }
    }

}
class Add_child_task {
    child_num;
    index;
    item_id;
    brother_object;
    brother_object_id;
    date_brother_id;
    //row:行数 index：第几个孩子 hierarchies：层次数 task_name: 任务名 item_id：上级行div的元素id
    //that.row_num,that.child_num,that.hierarchies,"child",item_id,that.child_item[that.child_num],this
    //row, index, hierarchies,task_name,item_id,brother_id
    //that.row_num,that.child_num,that.self_hierarchies,that.task_name,that.self_item_id,that.child_item_id[that.child_num]
    constructor(parent){
        this.row_num  = parent.row_num;  //第几行 与主任务同行
        this.index = parent.child_num;   //第几个子任务
        this.task_name = global.task_name;
        global.task_name = "null";
        this.hierarchies = parent.hierarchies+1; //父层次数
        this.item_id = []; //自身元素id
        for (let i = 0; i<9;i++){
            this.item_id.push(parent.item_id[i]+"_"+this.index);
        }

        this.brother_id = parent.child_item[this.index];//向下传递
        this.child_num =0;
        this.child_item = [this.item_id[0]];//行div记录列表上的兄弟 ，确定下一个的位置 自身为第一项
        this.child_object = [];
        this.row_div_id = this.item_id[0];
        this.date_id = this.row_div_id +"_date";
        this.flag_change = true;
        if(parent.child_object.length !== 0){
            this.brother_object = parent.child_object[parent.child_object.length-1];
            this.brother_object= this.brother_object.insert_position();
            this.brother_object_id = this.brother_object.item_id[0];
            this.date_brother_id = this.brother_object.date_id;
        }
        else{
            this.brother_object = parent;
            this.brother_object_id = this.brother_object.item_id[0];
            this.date_brother_id = this.brother_object.date_id;
        }
        this.brother_id = this.brother_object_id;
        // this.last_child_object = null;
        this.task_start_time = "null";
        this.task_end_time = "null";
        this.task_need_time = "null";
        this.div_left = 0;
        this.div_width = 0;
        this.parent_object = parent;

    }
    append_task() {
        let tree_view_row ="<div class= 'tree_view_row' isselected = 'true' id ='"+this.item_id[0]+"'></div>";
        //行开始部分
        let tree_view_row_item_first = "<div class= 'tree_view_row_item_first' id ='"+this.item_id[1]+"'></div>";
        let tree_view_row_item_first_icon0 = "<div class= 'tree_view_row_item_first_icon0 tree_file_subtract_icon tree_view_icon' id ='"+this.item_id[2]+"'></div>";
        let tree_view_row_item_first_icon1 = "<div class= 'tree_view_row_item_first_icon1 tree_file_merge_icon tree_view_icon' id ='"+this.item_id[3]+"'></div>";
        let tree_view_row_item_first_text = "<div class='tree_view_text' id='"+this.item_id[4]+this.child_num+"'>"+this.task_name+"</div>";
        //行结尾部分
        let tree_view_row_item_last = "<div class= 'tree_view_row_item_last' id ='"+this.item_id[5]+"'></div>";
        let tree_view_row_item_last_icon0 = "<div class= 'tree_view_row_item_last_icon0 tree_view_flag_icon tree_view_icon' id ='"+this.item_id[6]+"'></div>";
        let tree_view_row_item_last_text = "<div class='tree_view_row_item_last_text' id='"+this.item_id[7]+"'>1</div>";
        let tree_view_row_item_last_icon1 = "<div class= 'tree_view_row_item_last_icon1 tree_plus_icon tree_view_icon' id ='"+this.item_id[8]+"'></div>";
        console.log(tree_view_row);
        // $("#"+item_id[0]+"_"+index).insertAfter("#"+item_id[0]);
        // $("#tree_view_id").append(tree_view_row);
        // 以兄弟确定位置
        let that = this;
        $(tree_view_row).insertAfter($("#"+this.brother_id));
        // this.child_item.push(this.item_id[0]);  //入栈 列表上的兄弟
        $("#"+this.item_id[0]).append(tree_view_row_item_first, tree_view_row_item_last);
        //行首部
        let tree_row = $("#"+this.item_id[1]);
        tree_row.append(tree_view_row_item_first_icon0, tree_view_row_item_first_icon1, tree_view_row_item_first_text);
        tree_row.css("margin-left",+this.hierarchies*16+"px");
        $("#"+this.item_id[2]).click(function() {
            // this.alter_text = $("#tree_view_row_item_first_text_id"+index);
            $("#"+that.item_id[7]).text("zane");
            console.log(that.item_id[2]);
            if (that.child_object.length>0){
                if (that.flag_change){//隐藏
                    for (let value of that.child_object){
                        value.child_hide();
                    }
                    that.flag_change = false;
                    let child_item = $("#"+that.item_id[2]);
                    child_item.removeClass("tree_file_plus_icon");
                    child_item.addClass("tree_file_subtract_icon");
                }
                else{//显示
                    for (let value of that.child_object){
                        let row_id =  $("#"+value.row_div_id);
                        if(row_id.is(":hidden")) {
                            row_id.show();
                        }
                        let date_row_id = $("#"+value.date_id);
                        if (date_row_id.is(":hidden")){
                            date_row_id.show();
                        }
                    }
                    that.flag_change = true;
                    let child_item = $("#"+that.item_id[2]);
                    child_item.removeClass("tree_file_subtract_icon");
                    child_item.addClass("tree_file_plus_icon");
                }
            }
        });
        //行尾部
        console.log("#"+this.item_id[5]);
        $("#"+this.item_id[5]).append(tree_view_row_item_last_icon1, tree_view_row_item_last_text, tree_view_row_item_last_icon0);
        console.log("icon_1","#"+this.item_id[8]);
        $("#"+this.item_id[8]).click(function() {
            if (that.hierarchies>=5){
                alert ("目录层级不应超过最大数","The directory level should not exceed the maximum number");
            }
            else{
                $("#fade").css("display","block");
                $("#child_task_id").css("display","block");
                global.task_object = that;
                let tem = 0;
                // while (global.div_status){
                //     tem++;
                //     console.log(tem);
                // }
                // let new_tree_row = new Add_child_task(that);
                // new_tree_row.append_task();
                // new_tree_row.add_day();
                // new_tree_row.mouse_incident();
                // that.child_object.push(new_tree_row);
                // console.log("icon_1","#"+that.item_id[8],"true");
                // // that.brother_id = that.item_id[0]+"_"+that.child_num;
                // that.child_item.push(that.item_id[0]+"_"+that.child_num);  //入数组 列表上的兄弟
                // that.child_num = that.child_num +1; //child_item中项数 第二项目始为其创建的节点
                // console.log("1111111111111111111",that.brother_id,that.child_num)
            }
        });
        // alert(this.item_id);
        console.log(this.num);
    }
    // get nearest brother position for inserting
    add_day() {
        let year_days = task_date.distance_days(task_date.start_date,task_date.end_date);
        // alert(year_days);

        let row = this.index;
        let year = task_date.date_start_year;
        let start_month = task_date.date_start_month;
        let end_month = task_date.date_end_month;
        //行div
        let date_view_row = "<div id = '"+ this.row_div_id +"_date'  class = 'date_view_row'></div>";

        // $("#date_view_id").append(date_view_row);
        $(date_view_row).insertAfter($("#"+this.date_brother_id));

        let view_row = $("#"+ this.row_div_id +"_date");
        view_row.css("width",year_days*15+"px");
        for (let num = start_month; num <= end_month; num++) {
            let days = task_date.get_days(task_date.date_start_year, num, 0);
            let date_view_row_month = "<div id='"+this.row_div_id+"_date_" + num + "' class = 'date_view_row_month'></div>";
            let month_width = days * 15;
            view_row.append(date_view_row_month);
            let view_month = $("#"+this.row_div_id+"_date_" + num);
            view_month.css("width", month_width + "px");
            for (let da = 1; da <= days; da++) {
                let view_day = "<div id ='"+this.row_div_id+"_date_" + num + "_" + da + "' class='date_view_row_month_day'></div>";
                view_month.append(view_day);
                console.log(row, num, da);
            }
        }
    }
    slid_block() {
        let start_time = this.task_need_time.split("-")[0];
        let end_time = this.task_need_time.split("-")[1];
        // start_time = start_time.replace('/',"-");
        console.log("11122222222", start_time);
        let start_month = start_time.split("/")[0].split("0").pop();
        let start_day = start_time.split("/")[1].split("0").pop();
        let end_month = end_time.split("/")[0].split("0").pop();
        let end_day = end_time.split("/")[1].split("0").pop();
        console.log("44444444444", start_day, start_month, end_month, end_day, start_time, end_time);
        let start_date = task_date.date_start_year + "-" + start_month + "-" + start_day;
        let end_date = task_date.date_end_year + "-" + end_month + "-" + end_day;
        console.log(start_date, end_date);
        let days = task_date.distance_days(start_date, end_date);

        let left_days = task_date.distance_days(task_date.start_date, start_date);
        console.log(days, left_days);
        // start_month = parseInt(start_month);
        // start_day = parseInt(start_day);
        // end_month = parseInt(end_month);
        // end_day = parseInt(end_day);
        // console.log(end_day+start_day);
        // console.log("44444444444",start_day,start_month,end_month,end_day,start_time,end_time);
        // let days = 0;
        //
        // for (let i_month = start_month; i_month < end_month; i_month++){
        //     let temp_days=new Date(task_date.date_start_year,i_month,0);
        //     days = days+temp_days.getDate();
        //     console.log("for3333333333",days);//加结束月之前天数
        // }
        // let left_days = 0;
        // for (let left_month = task_date.date_start_month;left_month<= start_month;left_month++){
        //     let temp_days = new Date(task_date.date_start_year,i_month,0);
        // }
        // days = days + new Date(task_date.date_start_year,end_month,0);//结束月天数
        // days = days + end_day;
        // days = days -start_day+1;
        // console.log(days);
        let that = this;
        this.div_left = left_days*15;
        this.div_width = days*15;
        let sliding_block = "<div class='date_view_row_block' id ='" + this.date_id + "_block'></div>";
        let day_block_left = "<div class ='date_view_day_block_left' id='" + this.date_id + "_day_block_left'></div>";
        let day_block_right = "<div class ='date_view_day_block_right' id='" + this.date_id + "_day_block_right'></div>";
        $("#" + this.date_id).append(sliding_block);
        let row_block = $("#" + this.date_id + "_block");
        row_block.append(day_block_left, day_block_right);
        row_block.css("width", days * 15 + "px");
        row_block.css("left", left_days * 15 + "px");
        //绑定事件
        let day_block_left_hover = $("#" + this.date_id + "_day_block_left");
        let day_block_right_hover = $("#" + this.date_id + "_day_block_right");
        let add_width = 0;
        day_block_left_hover.hover(
            function () {
                day_block_left_hover.css("background","rgba(130,228,255,0.5)")
            },
            function () {
                day_block_left_hover.css("background","rgba(255, 232, 63, 0.5)")
            }
        );
        day_block_right_hover.hover(
            function () {
                day_block_right_hover.css("background","rgba(130,228,255,0.5)")
            },
            function () {
                day_block_right_hover.css("background","rgba(255, 232, 63, 0.5)")
            }
        );
        let move_width = 0;
        row_block.draggable({
            create: function (event, ui) {
            },
            drag: function (event, ui) {
                // day_block_left_hover.css("width","15px");
                // ui.position.left = Math.min( 100, ui.position.left );
                console.log("1111111", Math.round(ui.position.left / 15));
                // move_width=left_days*15-ui.position.left/15
                // row_block.css("left",ui.position.left+"px");
                // row_block.css("width",days*15-ui.position.left+"px");
            },
            axis: "x",
            grid: [15, 20],
            // minWidth : 15,
            containment:"parent",
        });
        row_block.resizable({
            create: function( event, ui ) {},
            containment: "parent",
            axis: "x",
            grid: 15,
            // handles:{'w':day_block_left_hover,
            //     "e":day_block_right_hover},
            handles:"w,e",
            resize: function (event, ui) {
                console.log("resize222222222222",Math.round(ui.position.left / 15));
                console.log("resize222222222222",ui.size.width);
            },
            stop: function (event,ui) {
                that.div_left = ui.position.left;
                that.div_width = ui.size.width;
                that.parent_object.alter_size(that.div_width,that.div_left);
            }
        });

        // day_block_right_hover.draggable({
        //     drag: function (event, ui) {
        //         row_block.css("left", Math.round(ui.position.left / 15) * 15 + "px");
        //         console.log("888888888888888888888",days * 15 + (left_days * 15 - Math.round(ui.position.left / 15) * 15) );
        //         // row_block.css("width", days * 15 + (left_days * 15 - Math.round(ui.position.left / 15) * 15) + "px");
        //     }
        // });
    }
    alter_size(current_width,current_left){
        let block_size = $("#" + this.date_id + "_block");
        let cur_width = 0;
        let cur_left = 0;
        if (current_width<this.div_left){
            cur_left = current_left;
            block_size.css("width",cur_left+"px");

        }
        if(current_width+current_left>this.div_width+this.div_left){
            cur_width = current_width+current_left -this.div_width+this.div_left;
            cur_width=cur_width +this.div_width;
            block_size.css("left",cur_width+"px");
        }
        if(this.parent_object){
            this.parent_object.alter_size(cur_width,cur_left);
        }
    }
    mouse_incident(){
        let current_id  = $("#"+this.row_div_id);
        let date_row_id = $("#"+this.date_id);
        current_id.hover(
            function () {
                current_id.css("background-color","#fafa25");
                date_row_id.css("background-color", "#fafa25");
            },
            function () {
                current_id.css("background-color","#838383");
                date_row_id.css("background-color", "#838383");
            }
        );
    }
    insert_position(){
        // let current_brother_object ;
        let that;
        if(this.child_object.length !== 0){
            that =  this.child_object[this.child_object.length - 1];
            that.insert_position();
        }
        else{
            that = this;
        }
        return that;
        // else{
        //     current_brother_object = this.brother_object;
        // }
    }
    //hide all item under self
    child_hide() {
        if (this.child_object.length !== 0) {
            for (let value of this.child_object) {
                value.child_hide();
            }
            this.flag_change = false;
        }
        $("#" + this.row_div_id).hide();
        $("#" + this.date_id).hide();
    }

    //显示子项D:\FFM_Code\ffm_chat
    child_show(){
        if (this.child_object.length!==0){
            for (let value of this.child_object){
                let row_id = $("#"+value.row_div_id);
                if(row_id.is(":hidden")){
                    row_id.show();
                }
            }
            this.flag_change = true;
        }
    }
}
//计数global variable
var global = {
    row_count : 0,
    color :"null",
    task_name :"null",
    date : "null",
    div_status:false,
    task_object:null,
};

function sendCode(thisBtn){
    let task_name = $("input[name='task_name'] ").val();
    // alert(task_name);
    if (task_name){
        // console.log(row_count, task_name);
        btn = thisBtn;
        let task = new Add_task(global.row_count,task_name);
        task.append_task(task.item_id);
        let add_view_day =new Add_day(global.row_count);
        task.mouse_incident();
        task.date_id = "date_view_row_"+global.row_count;
        console.log(global.row_count);
        global.row_count++;
    }
    document.getElementById('light').style.display='none';
    document.getElementById('fade').style.display='none';
}
function send_task() {
    global.task_name = $("input[id ='child_task_name_id']").val();
    global.date = $("input[id ='task_date_id']").val();
    alert(global.date);
    let that = global.task_object;
    let new_tree_row = new Add_child_task(that);
    new_tree_row.append_task();
    new_tree_row.add_day();
    new_tree_row.mouse_incident();
    new_tree_row.task_need_time = global.date;
    new_tree_row.slid_block();
    new_tree_row.parent_object.alter_size(new_tree_row.div_width,new_tree_row.div_left);
    that.child_object.push(new_tree_row);

    console.log("icon_1","#"+that.item_id[8],"true");
    // that.brother_id = that.item_id[0]+"_"+that.child_num;
    that.child_item.push(that.item_id[0]+"_"+that.child_num);  //入数组 列表上的兄弟
    that.child_num = that.child_num +1; //child_item中项数 第二项目始为其创建的节点
    console.log("1111111111111111111",that.brother_id,that.child_num)
    global.task_object = null;
    $("#child_task_id").css("display","none");
    $("#fade").css("display","none");
}
function quit(){
    document.getElementById('light').style.display='none';
    document.getElementById('fade').style.display='none';
    $("#child_task_id").css("display","none");
    // document.getElementById('child_task_id').style.display='none';
}

$(function(){
    initialization();
    add_time_header(task_date);
    $( "#task_date_id" ).daterangepicker();

    $("#tree_header_add_icon_id").click(function () {
        document.getElementById('light').style.display='block';
        document.getElementById('fade').style.display='block';
        $("input[name='task_name'] ").val("");
    });
});

// function add_tasks(index){
//     this.id= index;
//     var
//         // tree_view_row_id ="tree_view_row_id"+"_"+"index";
//         tree_view_row ="<div class= 'tree_view_row' id ='tree_view_row_id'></div>";
//         tree_view_row_item_first ="<div class= 'tree_view_row_item_first' id ='tree_view_row_item_first_id'></div>";
//         tree_view_row_item_last ="<div class= 'tree_view_row_item_last' id ='tree_view_row_item_last_id'></div>";
//         tree_view_row_item_first_icon0 ="<div class= 'tree_view_row_item_first_icon0 tree_subtract_icon' id ='tree_view_row_item_first_icon0_id'></div>";
//         tree_view_row_item_first_icon1 ="<div class= 'tree_view_row_item_first_icon1 tree_file_merge_icon' id ='tree_view_row_item_first_icon1_id'></div>";
//         tree_view_row_item_first_text ="<div class='tree_view_text' id='tree_view_row_item_first_text_id'>Text</div>";
//         $("#tree_view_id").append(tree_view_row);
//         $("#tree_view_row_id").append(tree_view_row_item_first, tree_view_row_item_last);
//         $("#tree_view_row_item_first_id").append(tree_view_row_item_first_icon0, tree_view_row_item_first_icon1, tree_view_row_item_first_text);
//     $("#tree_view_row_item_first_icon0").hide()
//     // $("tree_view_row_item_first").append(tree_view_row_item_first_icon0, tree_view_row_item_first_icon1);
// }


