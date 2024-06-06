var Host = ''
var TicketHost = 'https://q12301.com'

function req(host, url, data, method) {
    if (method === 'GET') {
        return axios.get(host + url, {
            params: data
        })
    } else if (method === 'POST') {
        return axios.post(host + url, data)
    }
}

function other_req(host, url, data, method) {
    if (method === 'GET') {
        return axios.get(url, {
            params: data
        })
    } else if (method === 'POST') {
        return axios.post(host + url, data)
    }
}

//登录接口
function SetLang(data) {
    return req(Host,'/i18n/setlang/', data, 'POST')
}

//登录接口
function LoginApi(data) {
    return req(Host,'/login_api', data, 'POST')
}


//注册接口
function RegApi(data) {
    return req(Host,'/reg_api', data, 'POST')
}

//数据接口
function DataApi(data) {
    return req(Host,'/get_data_api', data, 'GET')
}

//修改用户
function EditUser(data) {
    return req(Host,'/edit_user', data, 'POST')
}

//添加教程
function AddWord(data) {
    return req(Host,'/add_word', data, 'POST')
}

//获取教程列表
function GetWordList(data) {
    return req(Host,'/get_word_list', data, 'POST')
}

//获取教程
function GetWord(data) {
    return req(Host,'/get_word', data, 'POST')
}

//删除教程
function DelWord(data) {
    return req(Host,'/del_word', data, 'POST')
}


// 获取景区票列表
function getTicketList(data) {
    return req(TicketHost,'/service/mini-scenic-ticket-list-api/',data,'GET')
}
// 获取景区票详情
function getTicketDetail(data) {
    return req(TicketHost,'/service/mini-buy-ticket-detail-api/',data,'GET')
}
// 提交订单
function saveTicketOrder(data) {
    return req(TicketHost,'/service/web-save-buy-ticket-api/',data,'POST')
}
// 获取支付宝付款码
function ticketAliPayQrcode(data) {
    return req(TicketHost,'/ticket/agency-ticket-ali-pay-qrcode/',data,'GET')
}
// 获取微信付款码
function ticketWXPayQrcode(data) {
    return req(TicketHost,'/ticket/agency-ticket-pay-qrcode/',data,'GET')
}
// 获取支付状态
function salesOrderIsFinish(data) {
    return req(TicketHost,'/service/web-sales-order-is-finish-api/',data,'GET')
}
// 获取未来3天的入园流量
function getWaitingIn(data) {
    return other_req(TicketHost,'https://bigdata.q12301.com/big-data/get_waiting_in_v2/?scenic_id=2935878fd8bb472597058a92e8769f8d',data,'GET')
}
// 获取未来3天的入园流量
function getBasicNumberApi(data) {
    return other_req(TicketHost,'https://bigdata.q12301.com/big-data/get_basic_number_api/?scenic_id=2935878fd8bb472597058a92e8769f8d',data,'GET')
}