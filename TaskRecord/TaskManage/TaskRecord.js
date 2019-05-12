class Add_child_task {
    constructor(parent){
        if (parent === create_Main_task) {
            this.hierarchies =0;
        }
        else{
            if(parent.child_object.length !== 0){
                // this.brother_object = parent.child_object[parent.child_object.length-1];
                this.brother_object= parent.insert_position();
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
        this.child_ids =[];
        this.current_div_left =0;
        this.current_div_width = 0;
        this.append_task();
        // this.add_day();
        this.slid_block();//need parameter
        this.mouse_event();
    }
    append_task() {
        //ondrop= 'drop(event,this)' ondragover= 'allowDrop(event)' draggable='true' ondragstart='drag(event, this)'
        let tree_view_row ="<div class= 'tree_view_row' id ='"+this.item_id[0]+"' hierarchies ='"+this.hierarchies+"' obj ='"+global.div_num+"'></div>";
        //行开始部分
        let tree_view_row_item_first = "<div class= 'tree_view_row_item_first ' id ='"+this.item_id[1]+"' ></div>";
        let tree_view_row_item_first_icon0 = "<div class= 'tree_view_row_item_first_icon0 tree_file_subtract_icon tree_view_icon' id ='"+this.item_id[2]+"'></div>";
        let tree_view_row_item_first_icon1 = "<div class= 'tree_view_row_item_first_icon1 tree_file_merge_icon tree_view_icon' id ='"+this.item_id[3]+"'></div>";
        let tree_view_row_item_first_text = "<div class='tree_view_text' id='"+this.item_id[4]+"'>"+this.task_name+"</div>";
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
        // console.log("icon_1","#"+this.item_id[8]);
        $("#"+this.item_id[8]).click(function() {
            if (that.hierarchies>=4){
                alert ("目录层级不应超过最大数","The directory level should not exceed the maximum number");
            }
            else{
                let delete_task = $("#delete_task_id");
                delete_task.css('visibility', 'hidden');
                $("#fade").css("display","block");
                $("#child_task_id").css("display","block");
                $("input[id ='child_task_name_id']").focus();
                let task_need_time=$("#task_need_time_id");
                if (task_need_time.is(":hidden")){
                    task_need_time.show();
                }
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
        let date_view_row = "<div id = '"+ this.row_div_id +"_date'  class = 'date_view_row sliding_block_background'></div>";
        if(this.parent_object ===create_Main_task){
            $("#date_view_id").append(date_view_row);
        }
        else{
            $(date_view_row).insertAfter($("#"+this.date_brother_id));
        }
        // $("#date_view_id").append(date_view_row);
        let view_row = $("#"+ this.row_div_id +"_date");
        view_row.css("width",year_days*15+"px");
        // for (let num = start_month; num <= end_month; num++) {
        //     let days = task_date.get_days(task_date.date_start_year, num, 0);
        //     let date_view_row_month = "<div id='"+this.row_div_id+"_date_" + num + "' class = 'date_view_row_month'></div>";
        //     let month_width = days * 15;
        //     view_row.append(date_view_row_month);
        //     let view_month = $("#"+this.row_div_id+"_date_" + num);
        //     view_month.css("width", month_width + "px");
        //     for (let da = 1; da <= days; da++) {
        //         let view_day = "<div id ='"+this.row_div_id+"_date_" + num + "_" + da + "' class='date_view_row_month_day'></div>";
        //         view_month.append(view_day);
        //         // console.log(row, num, da);
        //     }
        // }
    }
    slid_block() {
        let year_days = task_date.distance_days(task_date.start_date,task_date.end_date)+1;
        //行div
        let date_view_row = "<div id = '"+ this.row_div_id +"_date'  class = 'date_view_row sliding_block_background'></div>";
        let date_view = $("#date_view_id");
        if(this.parent_object ===create_Main_task){
            date_view.append(date_view_row);
        }
        else{
            $(date_view_row).insertAfter($("#"+this.date_brother_id));
        }
        // $("#date_view_id").append(date_view_row);
        let view_row = $("#"+ this.row_div_id +"_date");
        view_row.css("width",year_days*15+"px");

        let start_time = this.task_need_time.split("-")[0];
        let end_time = this.task_need_time.split("-")[1];
        // start_time = start_time.replace('/',"-");
        let start_month = start_time.split("/")[0];
        let start_day = start_time.split("/")[1];
        let end_month = end_time.split("/")[0];
        let end_day = end_time.split("/")[1];
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
        this.current_div_left = this.div_left;
        let bar_left = this.div_left;
        let sliding_block = "<div class='date_view_row_block' id ='"+ this.date_id + "_block'></div>";
        let day_block_left = "<div class ='ui-resizable-handle ui-resizable-w' id='" + this.date_id + "_day_block_left' data-of_object= 'that'></div>";
        let day_block_right = "<div class ='ui-resizable-handle ui-resizable-e' id='" + this.date_id + "_day_block_right'></div>";

        // console.log(date_view.scrollLeft());
        if(this.div_left>=60){
            bar_left=bar_left -60;
            $(".date_all").scrollLeft(bar_left);
        }
        else{
            $(".date_all").scrollLeft(bar_left);
        }
        view_row.append(sliding_block);
        let row_block = $("#" + this.date_id + "_block");
        row_block.append(day_block_left,day_block_right);


        // row_block.append(day_block_left, day_block_right);
        // console.log(row_block);
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
    alter_father_sliding_length(){
        if(this.child_object.length>=1){
            let cur_smallest_left = 5475;
            let cur_max_right = 0;
            for(let value of this.child_object){
               if (cur_smallest_left> value.div_left){
                   cur_smallest_left = value.div_left;
               }
               if(value.div_left+value.div_width>cur_max_right){
                   cur_max_right = value.div_left+value.div_width;
               }
            }
            this.div_left = cur_smallest_left;
            this.div_width = cur_max_right - this.div_left;
            let sliding_block = $("#"+ this.date_id + '_block');
            sliding_block.css("left",this.div_left+"px");
            sliding_block.css("width",this.div_width+'px');
            // sliding_block.text(this.div_width/15);
            // console.log(this,this.div_left,this.div_width);
            if(this.parent_object!==create_Main_task){
                this.parent_object.alter_father_sliding_length();
            }
        }
        $("#"+this.item_id[7]).text(this.div_width/15);

    }

    alter_child_sliding_length_drag(change_left){
        if (this.child_object.length>=1){
            for (let value of this.child_object){
                value.div_left =value.div_left+change_left;
                $("#"+ value.date_id + '_block').css("left",value.div_left+"px");
                value.alter_child_sliding_length_drag(change_left);
            }
        }
    }
    alter_sliding_block(unchanged_direction,unchanged_length,changed_ratio){
        let current_left =0;
        let current_width = 0;
        if(this.child_object.length>=1){
            for(let value of this.child_object){
                switch (unchanged_direction) {
                    case "left":
                        current_left = (value.div_left - unchanged_length)*changed_ratio+unchanged_length;
                        current_width = value.div_width*changed_ratio;
                        break;
                    case "right":
                        current_left = unchanged_length-(unchanged_length-value.div_left-value.div_width)*changed_ratio-value.div_width*changed_ratio;
                        current_width  = value.div_width*changed_ratio;
                        break;
                }
                current_left = Math.floor(value.div_left/15)*15;  //向下取整
                current_width = Math.ceil(value.div_width/15)*15;//向上
                if(current_width<15){
                    current_width = 15;
                }
                let sliding_block = $("#"+ value.date_id + '_block');
                sliding_block.css("left",current_left+'px');
                sliding_block.css("width",current_width+'px');
                this.current_div_left = current_left;
                this.current_div_width = current_width;
                value.alter_child_sliding_length_current_resize(unchanged_direction,unchanged_length,changed_ratio)
            }
        }
    }
    alter_child_sliding_length_resize(unchanged_direction,unchanged_length,changed_ratio){
        switch (unchanged_direction) {
            case  "left":
                if(this.child_object.length>=1){
                    for(let value of this.child_object){
                        value.div_left = (value.div_left - unchanged_length)*changed_ratio+unchanged_length;
                        value.div_width = value.div_width*changed_ratio;
                        value.div_left = Math.floor(value.div_left/15)*15;  //向下取整
                        value.div_width = Math.ceil(value.div_width/15)*15;//向上
                        if(value.div_width<15){
                            value.div_width = 15;
                        }
                        let sliding_block = $("#"+ value.date_id + '_block');
                        sliding_block.css("left",value.div_left+'px');
                        sliding_block.css("width",value.div_width+'px');
                        $("#"+value.item_id[7]).text(value.div_width/15);
                        // sliding_block.text(value.div_width/15);
                        value.alter_child_sliding_length_resize(unchanged_direction,unchanged_length,changed_ratio)
                    }
                }
                break;
            case  "right":
                if(this.child_object.length>=1){
                    for(let value of this.child_object){
                        value.div_left = unchanged_length-(unchanged_length-value.div_left-value.div_width)*changed_ratio-value.div_width*changed_ratio;
                        value.div_width  = value.div_width*changed_ratio;
                        value.div_left = Math.floor(value.div_left/15)*15;  //向下取整
                        value.div_width = Math.ceil(value.div_width/15)*15;//向上
                        if(value.div_width<15){
                            value.div_width = 15;
                        }
                        let sliding_block = $("#"+ value.date_id + '_block');
                        sliding_block.css("left",value.div_left+'px');
                        sliding_block.css("width",value.div_width+'px');
                        $("#"+value.item_id[7]).text(value.div_width/15);
                        // sliding_block.text(value.div_width/15);
                        value.alter_child_sliding_length_resize(unchanged_direction,unchanged_length,changed_ratio)
                    }
                }
                break;
        }
    }
    mouse_event(){
        let current_obj1 = null;
        let current_obj2 = null;
        let that =this;
        let current_id  = $("#"+this.row_div_id);
        let date_row_id = $("#"+this.date_id);
        let text_alter = $("#"+this.item_id[4]);//alter text
        let sliding_block_handle_w = $("#" + this.date_id + "_day_block_left");
        let sliding_block_handle_e = $("#" + this.date_id + "_day_block_right");
        let row_block = $("#" + this.date_id + "_block");
        sliding_block_handle_w.css("left",'0');
        sliding_block_handle_e.css('right','0');
        current_id.hover(
            function () {
                current_id.css("background-color","#999");
                date_row_id.css("background-color", "#999");
            },
            function () {
                current_id.css("background-color","inherit");
                date_row_id.css("background-color", "inherit");
            }
        );
        current_id.draggable({
            cursor: "move",
            // revert: "invalid",
            revert:true,
            // helper: "clone",
            axis:"y",
            // revertDuration: 200
            // group: [$("#drag1"),$("#drag2") ]
        });
        current_id.droppable({
            accept: ".tree_view_row",
            // activeClass: "ui-state-hover",
            // hoverClass: "ui-state-active",
            activeClass: "ui_state_active",
            hoverClass: "ui_drop_hover",
            drop: function( event, ui ) {
                // console.log(ui.position.left,ui.position.top);
                let drag_div = ui.draggable, drop_div = $(this);
                // let temp_drag = drag_div.children(":first").children(":last").text();
                // let temp_drop = drop_div.children(":first").children(":last").text();
                // let drag_time = drag_div.children(":last").children(".tree_view_row_item_last_text").text()*15;
                // let drop_time = drop_div.children(":last").children(".tree_view_row_item_last_text").text()*15;
                // if(drag_div.attr("hierarchies")!==drop_div.attr("hierarchies")){
                //
                // }
                let obj_drag = global.div_object[drag_div.attr("obj")];
                let obj_drop = global.div_object[drop_div.attr("obj")];
                // if(obj_drag.parent_object !== create_Main_task){
                //     obj_drag = obj_drag.parent_object;
                // }
                // if(obj_drop.parent_object !== create_Main_task ){
                //     obj_drop= obj_drop.parent_object;
                // }
                let level_dis = 0;
                if (drop_div.attr("hierarchies")>drag_div.attr("hierarchies")){
                    level_dis = drop_div.attr("hierarchies")-drag_div.attr("hierarchies");
                    obj_drag = obj_drag.parent_object;
                }
                else if (drag_div.attr("hierarchies")>drop_div.attr("hierarchies")){
                    level_dis = drag_div.attr("hierarchies")-drop_div.attr("hierarchies");
                    for (let i =0; i<=level_dis;i++){
                        if ( obj_drop.parent_object!==create_Main_task) {
                            obj_drop =obj_drop.parent_object;
                        }
                    }
                }
                if(obj_drag!==obj_drop){
                    that.insert_into(global.div_object[drag_div.attr("obj")]);
                }
                else{
                    that.insert_into(global.div_object[drag_div.attr("obj")]);
                }
                let child_num = 0;
                if (obj_drag.parent_object !==null){
                    child_num= obj_drag.parent_object.child_object.length;
                }

                let first_child = 0;
                for (let num= 0; num<child_num;num++){
                    if (obj_drag.parent_object.child_object[num] === obj_drag){
                        first_child = num;
                    }
                }
                obj_drag.parent_object.child_object.splice(first_child,1)
                // if(drag_div.attr("hierarchies")!==drop_div.attr("hierarchies")){
                //     drag_div.children(":first").children(":last").text(temp_drop);
                //     drop_div.children(":first").children(":last").text(temp_drag);
                //     drop_div.children(":last").children(".tree_view_row_item_last_text").text(drag_time/15);
                //     drag_div.children(":last").children(".tree_view_row_item_last_text").text(drop_time/15);
                //     // console.log("11111",global.div_object[drag_div.attr("obj")].div_width);
                //     global.div_object[drag_div.attr("obj")].div_width = drop_time;
                //     global.div_object[drop_div.attr("obj")].div_width = drag_time;
                //     $("#"+global.div_object[drop_div.attr("obj")].date_id+"_block").css("width",drag_time+"px");
                //     $("#"+global.div_object[drag_div.attr("obj")].date_id+"_block").css("width",drop_time+"px");
                //     if(global.div_object[drag_div.attr("obj")].child_object.length>=1){
                //         global.div_object[drag_div.attr("obj")].alter_father_sliding_length();
                //     }
                //     else{
                //         if(global.div_object[drag_div.attr("obj")].parent_object !==create_Main_task){
                //             global.div_object[drag_div.attr("obj")].parent_object.alter_father_sliding_length();
                //         }
                //     }
                //     if(global.div_object[drop_div.attr("obj")].child_object.length>=1){
                //         global.div_object[drop_div.attr("obj")].alter_father_sliding_length();
                //     }
                //     else{
                //         if(global.div_object[drop_div.attr("obj")].parent_object!== create_Main_task){
                //             global.div_object[drag_div.attr("obj")].parent_object.alter_father_sliding_length();
                //         }
                //     }
                // }
                // else{
                //     console.log(drag_div.position.top,drop_div.position.top);
                // }
                // dragPos = drag_div.position(), dropPos = drop_div.position();
                // ui.helper.children(":first").children(":last").text(temp_drop);
            },
            // deactivate: function (event,ui) {
            //
            // }
        });
        // current_id.sortable({
        //
        // });
        // function allowDrop(ev) {
        //     ev.preventDefault();
        // }
        // current_id.draggable ="true";
        // current_id.onselectstart = function(){
        //     return false
        // }
        //     .ondragstart = function(ev){
        //         current_obj1 = this;
        //         ev.preventDefault();
        // }
        //     .ondragend = function(ev){
        //
        // }
        //     .ondragover = function(ev){
        //
        // }
        //     .ondragenter = function(ev){
        //
        // }
        //     .ondrop = function(ev){
        //         ev.preventDefault();
        //         print(this);
        //         let cur_id = current_obj1.id;
        //         current_obj1.id = this.id;
        //     srcdiv = divdom;
        //     temp = divdom.innerHTML;
        // };
        text_alter.on("dblclick",function(){
            let inputElement = document.createElement("input");
            //get div text value
            inputElement.type ="text";
            inputElement.id = "name_input";
            inputElement.className= "name_input";
            // $("#name_input").css("width","50px").css("height","18px");
            // console.log(inputElement);
            inputElement.value = this.innerHTML;
            // inputElement.style="maxlength:18px,width:50px";
            //replace div with input
            this.parentNode.replaceChild(inputElement, this);
            let that =this;
            inputElement.focus();
            // 当inputElement失去焦点时触发下面函数，使得input变成div
            inputElement.onblur = function() {
                //pass input value to div
                that.innerHTML = inputElement.value;
                //用原来的div重新替换inputElement
                inputElement.parentNode.replaceChild(that, inputElement);
            };
        });
        row_block.hover(
            function (){
                sliding_block_handle_w.css("background","rgb(223,255,86)");
                sliding_block_handle_e.css("background","rgb(223,255,86)");
            },
            function () {
                sliding_block_handle_w.css("background","inherit");
                sliding_block_handle_e.css("background","inherit");
            }
            );
        row_block.draggable({
            cursor:"move",
            create: function (event, ui) {
            },
            drag: function (event, ui) {
                let change_left= ui.position.left - that.div_left;
                that.div_left = Math.round(ui.position.left/15)*15;
                row_block.css("left", Math.round(ui.position.left/15)*15+"px");
                if (that.parent_object!==create_Main_task){
                    that.parent_object.alter_father_sliding_length();
                }
                change_left = Math.round(change_left/15)*15;
                that.alter_child_sliding_length_drag(change_left);
            },
            scroll: true,
            axis: "x",
            grid: [15, 20],
            // minWidth : 15,
            containment:"parent",
            stop: function (event,ui) {

            }
        });
        let unchanged_direction = "";
        let changed_ratio=1;
        let unchanged_length = 0;
        row_block.resizable({
            cursor: "auto",
            create: function( event, ui ) {},
            containment: "parent",
            axis: "x",
            grid: 15,
            // handles:{'w':day_block_left_hover,
            //     "e":day_block_right_hover},
            handles:{
                'w': "#" + this.date_id + "_day_block_left",
                'e': "#" + this.date_id + "_day_block_right"
            },
            resize: function (event, ui) {
                // console.log("resize222222222222",Math.round(ui.position.left / 15));
                // console.log("resize222222222222",ui.size.width);
                // status = true;
                // changed_ratio = ui.size.width/that.div_width;
            },
            stop: function (event,ui) {
                changed_ratio = ui.size.width/that.div_width;
                if(that.div_left===ui.position.left){
                    unchanged_length = that.div_left;
                    unchanged_direction = "left";
                    that.alter_child_sliding_length_resize(unchanged_direction,unchanged_length,changed_ratio)

                }
                else{
                    unchanged_length = that.div_left+that.div_width;
                    unchanged_direction = "right";
                    that.alter_child_sliding_length_resize(unchanged_direction,unchanged_length,changed_ratio)
                }
                that.div_left = ui.position.left;
                that.div_width = ui.size.width;
                if (that.parent_object!==create_Main_task){
                    that.parent_object.alter_father_sliding_length();
                }
                // that.div_left =that.current_div_left;
                // that.div_width = that .current_div_width;
                // status = false;
                // that.alter_child_sliding_length_resize(unchanged_direction,unchanged_length,changed_ratio,status);
                $("#"+that.item_id[7]).text(that.div_width/15);
                // row_block.text(that.div_width/15);
            }
        });
        // let flag = $("#"+this.item_id[6]);
        // flag.hover(function() {
        //     let dialog_left =flag.position().left+300;
        //     console.log(flag.position());
        //     console.log(flag);
        //
        //     let dialog_top = flag.position().top+80;
        //     // $(".popup_dialog").css('visibility', 'visible');
        //     console.log("hover1111",dialog_top,dialog_left);
        //     $(".popup_dialog").animate({opacity: "show", left: dialog_left, top: dialog_top}, "slow");
        // }, function() {
        //     $(".popup_dialog").animate({opacity: "hide", top: "-85"}, "fast");
        // });
    }
    insert_into(old_obj){
        let that =this;
        if (that.hierarchies!==8){
            let add_obj = new Add_child_task(that);
            that.child_object.push(add_obj);
            that.child_num = that.child_num +1; //child_item中项数 第二项目始为其创建的节点
            add_obj.div_left = old_obj.div_left;
            add_obj.div_width = old_obj.div_width;
            $("#"+add_obj.date_id+"_block").css({
                left: add_obj.div_left+"px",
                width: add_obj.div_width+"px",
            });
            that.alter_father_sliding_length();
            let temp = $("#"+old_obj.item_id[4]).text();
            $("#"+add_obj.item_id[4]).text(temp);
            global.div_object.push(add_obj);
            global.div_num = global.div_num+1;
            if(old_obj.child_object.length>=1){
                for(let num = 0; num<old_obj.child_object.length; num++){
                    add_obj.insert_into(old_obj.child_object[num]);
                }
            }
            $("#"+old_obj.row_div_id).remove();
            $("#"+old_obj.date_id).remove();
        }
        else{
            alert("level can't surpass 20");
        }


    }

    // child_id(obj){
    //     this.child_ids.push(obj.row_div_id);
    //     if(obj.child_object !== null){
    //         for(let num =0; num< old.child_object.length; num++){
    //             child_id(obj.child_object[num])
    //         }
    //     }
    // }
    //
    insert_position(){
        let that;
        if(this.child_object.length !== 0){
            that =  this.child_object[this.child_object.length - 1];
            that = that.insert_position();
        }
        else{
            that = this;
        }
        return that;
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
