class Add_child_task {

    constructor(parent){

        if (parent === create_Main_task) {
            this.hierarchies =0;
        }
        else{
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
            this.hierarchies = parent.hierarchies+1; //父层次数
            this.task_level = false;
            // this.brother_id = parent.child_item[this.index];//向下传递
        }
        this.parent_object = parent;
        this.row_num  = parent.row_num;  //第几行 与主任务同行
        this.index = parent.child_num;   //第几个子任务

        this.item_id = []; //自身元素id
        for (let i = 0; i<9;i++){
            this.item_id.push(parent.item_id[i]+"_"+this.index);
        }
        this.child_item = [this.item_id[0]];//行div记录列表上的兄弟 ，确定下一个的位置 自身为第一项
        this.task_date = [];
        this.child_num =0;
        this.child_object = [];
        this.row_div_id = this.item_id[0];
        this.date_id = this.row_div_id +"_date";
        this.flag_change = false;
        // this.last_child_object = null;
        this.task_name = global.task_name;
        this.task_need_time = global.date;
        this.div_left = 0;
        this.div_width = 0;

        this.append_task();
        this.add_day();
        this.slid_block();//need parameter
        this.mouse_event();
    }
    append_task() {
        let tree_view_row ="<div class= 'tree_view_row' id ='"+this.item_id[0]+"'></div>";
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
        // console.log(tree_view_row);
        // $("#"+item_id[0]+"_"+index).insertAfter("#"+item_id[0]);
        // $("#tree_view_id").append(tree_view_row);
        // 以兄弟确定位置
        let that = this;
        if(this.parent_object === create_Main_task){
            $("#tree_view_id").append(tree_view_row);
        }
        else{
            $(tree_view_row).insertAfter($("#"+this.brother_id));
        }
        // this.child_item.push(this.item_id[0]);  //入栈 列表上的兄弟
        $("#"+this.item_id[0]).append(tree_view_row_item_first, tree_view_row_item_last);
        //行首部
        let tree_row = $("#"+this.item_id[1]);
        tree_row.append(tree_view_row_item_first_icon0, tree_view_row_item_first_icon1, tree_view_row_item_first_text);
        tree_row.css("margin-left",+this.hierarchies*16+"px");
        $("#"+this.item_id[2]).click(function() {
            // this.alter_text = $("#tree_view_row_item_first_text_id"+index);
            // console.log(that.item_id[2]);
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
        // console.log("#"+this.item_id[5]);
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
            }
        });
        // alert(this.item_id);
    }
    // get nearest brother position for inserting
    add_day() {
        let year_days = task_date.distance_days(task_date.start_date,task_date.end_date)+1;
        let row = this.index;
        let year = task_date.date_start_year;
        let start_month = task_date.date_start_month;
        let end_month = task_date.date_end_month;
        //行div
        let date_view_row = "<div id = '"+ this.row_div_id +"_date'  class = 'date_view_row'></div>";
        if(this.parent_object ===create_Main_task){
            $("#date_view_id").append(date_view_row);
        }
        else{
            $(date_view_row).insertAfter($("#"+this.date_brother_id));
        }
        // $("#date_view_id").append(date_view_row);
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
                // console.log(row, num, da);
            }
        }
    }
    slid_block() {
        let start_time = this.task_need_time.split("-")[0];
        let end_time = this.task_need_time.split("-")[1];
        // start_time = start_time.replace('/',"-");
        let start_month = start_time.split("/")[0].split("0").pop();
        let start_day = start_time.split("/")[1].split("0").pop();
        let end_month = end_time.split("/")[0].split("0").pop();
        let end_day = end_time.split("/")[1].split("0").pop();
        let start_date = task_date.date_start_year + "-" + start_month + "-" + start_day;
        let end_date = task_date.date_end_year + "-" + end_month + "-" + end_day;

        let days = task_date.distance_days(start_date, end_date)+1;
        let left_days = task_date.distance_days(task_date.start_date, start_date);
        // console.log(start_date, end_date);
        // console.log(days, left_days);
        $("#"+this.item_id[7]).text(days);

        let that = this;
        this.task_date=[start_date,end_date];
        this.div_left = left_days*15;
        this.div_width = days*15;

        let sliding_block = "<div class='date_view_row_block' id ='"+ this.date_id + "_block'></div>";
        let day_block_left = "<div class ='date_view_day_block_left' id='" + this.date_id + "_day_block_left'></div>";
        let day_block_right = "<div class ='date_view_day_block_right' id='" + this.date_id + "_day_block_right'></div>";



        $("#" + this.date_id).append(sliding_block);
        let row_block = $("#" + this.date_id + "_block");
        row_block.append(day_block_left,day_block_right);

        // row_block.append(day_block_left, day_block_right);
        console.log(row_block);
        row_block.css("width", days * 15 + "px");
        row_block.css("left", left_days * 15 + "px");
        //绑定事件

    }

    alter_date(child_start_date,child_end_date){
        let block_size = $("#" + this.date_id + "_block");
        let cur_width = 0;
        let revamp_width = 0;
        let cur_left = 0;
        if (this.child_object.length>1) {
            if (child_start_date < this.task_date[0]) {
                revamp_width = task_date.distance_days(child_start_date, this.task_date[0]) * 15;
                this.task_date[0] = child_start_date;
                this.div_left = this.div_left - revamp_width;
                this.div_width = this.div_width + revamp_width;
                block_size.css("width", this.div_width + "px");
                block_size.css("left", this.div_left + "px");
            }
            if (child_end_date > this.task_date[1]) {
                revamp_width = task_date.distance_days(this.task_date[1], child_end_date) * 15;
                this.div_width = this.div_width + revamp_width;
                block_size.css("width", this.div_width + "px");
            }
        }
        else{
            this.task_date[0] = child_start_date;
            this.task_date[1] = child_end_date;
            this.div_left = task_date.distance_days(task_date.start_date,this.task_date[0])*15;
            this.div_width = task_date.distance_days(this.task_date[0],this.task_date[1])*15+15;
            block_size.css("width", this.div_width + "px");
            block_size.css("left", this.div_left + "px");
        }
    }

    mouse_event(){
        let that =this;
        let current_id  = $("#"+this.row_div_id);
        let date_row_id = $("#"+this.date_id);
        let day_block_left_hover = $("#" + this.date_id + "_day_block_left");
        let day_block_right_hover = $("#" + this.date_id + "_day_block_right");
        let row_block = $("#" + this.date_id + "_block");
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
        row_block.draggable({
            create: function (event, ui) {
            },
            drag: function (event, ui) {
                // day_block_left_hover.css("width","15px");
                // ui.position.left = Math.min( 100, ui.position.left );
                // console.log("1111111", Math.round(ui.position.left / 15));
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
                // console.log("resize222222222222",Math.round(ui.position.left / 15));
                // console.log("resize222222222222",ui.size.width);
            },
            stop: function (event,ui) {
                that.div_left = ui.position.left;
                that.div_width = ui.size.width;
                // alter("father_task's date alter function not yet append please ")
                // that.parent_object.alter_date(that.task_date[0],that.task_date[1]);
            }
        });
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
