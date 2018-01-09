/**
 * Created by gogo on 17-7-12.
 */
/*$(function () {
    var add_url = $('#add_url').text();
    var $show_count = $('#show_count');
    var select_goods = [];
    $('.add_goods').click(function () {
        // 在列表也点击购物车

        var good_id = $(this).attr('id');
        //console.log(goods_id);
        var goods_num = parseInt($show_count.text());
        select_goods.push(good_id);
        console.log(select_goods);
        $('.cart_name').attr('id',good_id);
        $show_count.text(goods_num + 1);

        // $.post("{% url 'shopping_list' %}",{'select_good':good_id},function (callback) {
        //         console.log(callback);
        // })

        $.post("{% url 'shop:shopping_list' %}",{'select_good':1,'csrfmiddlewaretoken':"{{ csrf_token }}"}, function(callback){
                console.log('helo,123');}
            )


        // $('.cart_name').attr('id',goods_id)
        //data = {'buy_num': 1};
        // $.get(add_url, data, function (data) {
        //     if (data.statue === "0") {
        //         alert('服务器出错,添加错误')
        //     }
        // })

    });
});
*/
