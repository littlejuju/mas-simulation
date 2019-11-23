tick_time = 3
seed = 1992
ticks = 81
ad_budget_ration = 0.7
relevance_to_recommend = 0.3
email_body = '''<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8"> <!-- utf-8 works for most cases -->
<meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
<meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
<meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
<title></title> <!-- The title tag shows in email notifications, like Android 4.4. -->


<link href="https://fonts.googleapis.com/css?family=Playfair+Display:400,400i,700,700i" rel="stylesheet">

<!-- CSS Reset : BEGIN -->
<style>

html,
body {
    margin: 0 auto !important;
padding: 0 !important;
height: 100% !important;
width: 100% !important;
background: #f1f1f1;
}

/* What it does: Stops email clients resizing small text. */
* {
    -ms-text-size-adjust: 100%;
-webkit-text-size-adjust: 100%;
}

/* What it does: Centers email on Android 4.4 */
div[style*="margin: 16px 0"] {
    margin: 0 !important;
}

/* What it does: Stops Outlook from adding extra spacing to tables. */
table,
td {
    mso-table-lspace: 0pt !important;
mso-table-rspace: 0pt !important;
}

/* What it does: Fixes webkit padding issue. */
table {
    border-spacing: 0 !important;
border-collapse: collapse !important;
table-layout: fixed !important;
margin: 0 auto !important;
}

/* What it does: Uses a better rendering method when resizing images in IE. */
img {
    -ms-interpolation-mode:bicubic;
}

/* What it does: Prevents Windows 10 Mail from underlining links despite inline CSS. Styles for underlined links should be inline. */
a {
    text-decoration: none;
}

/* What it does: A work-around for email clients meddling in triggered links. */
*[x-apple-data-detectors],  /* iOS */
.unstyle-auto-detected-links *,
.aBn {
    border-bottom: 0 !important;
cursor: default !important;
color: inherit !important;
text-decoration: none !important;
font-size: inherit !important;
font-family: inherit !important;
font-weight: inherit !important;
line-height: inherit !important;
}

/* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */
.a6S {
    display: none !important;
opacity: 0.01 !important;
}

/* What it does: Prevents Gmail from changing the text color in conversation threads. */
.im {
    color: inherit !important;
}

/* If the above doesn't work, add a .g-img class to any image in question. */
img.g-img + div {
    display: none !important;
}

/* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
/* Create one of these media queries for each additional viewport size you'd like to fix */

/* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
@media only screen and (min-device-width: 320px) and (max-device-width: 374px) {
    u ~ div .email-container {
    min-width: 320px !important;
}
}
/* iPhone 6, 6S, 7, 8, and X */
@media only screen and (min-device-width: 375px) and (max-device-width: 413px) {
    u ~ div .email-container {
    min-width: 375px !important;
}
}
/* iPhone 6+, 7+, and 8+ */
@media only screen and (min-device-width: 414px) {
    u ~ div .email-container {
    min-width: 414px !important;
}
}

</style>

<!-- CSS Reset : END -->

<!-- Progressive Enhancements : BEGIN -->
<style>

.primary{
    background: #f3a333;
}

.bg_white{
    background: #ffffff;
}
.bg_light{
    background: #fafafa;
}
.bg_black{
    background: #000000;
}
.bg_dark{
    background: rgba(0,0,0,.8);
}
.email-section{
    padding:2.5em;
}

/*BUTTON*/
.btn{
    padding: 10px 15px;
}
.btn.btn-primary{
    border-radius: 30px;
background: #f3a333;
color: #ffffff;
}



h1,h2,h3,h4,h5,h6{
    font-family: 'Playfair Display', serif;
color: #000000;
margin-top: 0;
}

body{
    font-family: 'Montserrat', sans-serif;
font-weight: 400;
font-size: 15px;
line-height: 1.8;
color: rgba(0,0,0,.4);
}

a{
    color: #f3a333;
}

table{
}
/*LOGO*/

.logo h1{
    margin: 0;
}
.logo h1 a{
    color: #000;
        font-size: 20px;
font-weight: 700;
text-transform: uppercase;
font-family: 'Montserrat', sans-serif;
}

/*HERO*/
.hero{
    position: relative;
}
.hero img{

}
.hero .text{
    color: rgba(255,255,255,.8);
}
.hero .text h2{
    color: #ffffff;
        font-size: 30px;
margin-bottom: 0;
}


/*HEADING SECTION*/
.heading-section{
}
.heading-section h2{
    color: #000000;
        font-size: 28px;
margin-top: 0;
line-height: 1.4;
}
.heading-section .subheading{
    margin-bottom: 20px !important;
display: inline-block;
font-size: 13px;
text-transform: uppercase;
letter-spacing: 2px;
color: rgba(0,0,0,.4);
position: relative;
}
.heading-section .subheading::after{
    position: absolute;
left: 0;
right: 0;
bottom: -10px;
content: '';
width: 100%;
height: 2px;
background: #f3a333;
margin: 0 auto;
}

.heading-section-white{
    color: rgba(255,255,255,.8);
}
.heading-section-white h2{
    font-size: 28px;
font-family:
line-height: 1;
padding-bottom: 0;
}
.heading-section-white h2{
    color: #ffffff;
}
.heading-section-white .subheading{
    margin-bottom: 0;
display: inline-block;
font-size: 13px;
text-transform: uppercase;
letter-spacing: 2px;
color: rgba(255,255,255,.4);
}


.icon{
    text-align: center;
}
.icon img{
}


/*SERVICES*/
.text-services{
    padding: 10px 10px 0;
text-align: center;
}
.text-services h3{
    font-size: 20px;
}

/*BLOG*/
.text-services .meta{
    text-transform: uppercase;
font-size: 14px;
}

/*TESTIMONY*/
.text-testimony .name{
    margin: 0;
}
.text-testimony .position{
    color: rgba(0,0,0,.3);

}


/*VIDEO*/
.img{
    width: 100%;
height: auto;
position: relative;
}
.img .icon{
    position: absolute;
top: 50%;
left: 0;
right: 0;
bottom: 0;
margin-top: -25px;
}
.img .icon a{
    display: block;
width: 60px;
position: absolute;
top: 0;
left: 50%;
margin-left: -25px;
}



/*COUNTER*/
.counter-text{
    text-align: center;
}
.counter-text .num{
    display: block;
color: #ffffff;
font-size: 34px;
font-weight: 700;
}
.counter-text .name{
    display: block;
color: rgba(255,255,255,.9);
font-size: 13px;
}


/*FOOTER*/

.footer{
    color: rgba(255,255,255,.5);

}
.footer .heading{
    color: #ffffff;
        font-size: 20px;
}
.footer ul{
    margin: 0;
padding: 0;
}
.footer ul li{
    list-style: none;
margin-bottom: 10px;
}
.footer ul li a{
    color: rgba(255,255,255,1);
}


@media screen and (max-width: 500px) {

    .icon{
    text-align: left;
}

.text-services{
    padding-left: 0;
padding-right: 20px;
text-align: left;
}

}

</style>


</head>

<body width="100%" style="margin: 0; padding: 0 !important; mso-line-height-rule: exactly; background-color: #222222;">
<center style="width: 100%; background-color: #f1f1f1;">
<div style="display: none; font-size: 1px;max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
</div>
<div style="max-width: 800px; margin: 0 auto;" class="email-container">
<!-- BEGIN BODY -->
<table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
<tr>
<td class="bg_white logo" style="padding: 3em 2.5em; text-align: center; background-image: url(https://wx4.sinaimg.cn/mw690/b016a00egy1g70i0xcu89j21ak06tdh0.jpg); background-size: 100% 100%">
</td>
</tr><!-- end tr -->
<tr>
<td valign="middle" class="hero" style="background-image: url(https://wx2.sinaimg.cn/mw690/b016a00egy1g70gwbq8cvj20gs09g3zh.jpg); background-size: cover; height: 400px;">
<table>
<tr>
<td>
<div class="text" style="padding: 0 3em; text-align: center;">
<h2>We serve best data analysis service!</h2>
<h3 style="color: #f1f1f1">Data package has been shared to you through Google Spread Sheet</p>
</div>
</td>
</tr>
</table>
</td>
</tr><!-- end tr -->
<tr>
<td class="bg_white email-section">
<div class="heading-section" style="text-align: center; padding: 0 30px;">
<span class="subheading"></span>
<h2>Hi seller.name</h2>
<p>Here are all data sheets you require :)</p>
                                            </div>
                                              <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                                                                                                                          <tr>
                                                                                                                          <td valign="top" width="50%" style="padding-top: 20px;">
                                                                                                                                                             <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                                                                                                                                                                                                                         <tr>
                                                                                                                                                                                                                                         <td class="icon">
<img src="https://wx3.sinaimg.cn/mw690/b016a00egy1g97ze666hkj20l90by41o.jpg" alt="" style="width: 450px; max-width: 600px; height: auto; margin: auto; display: block;">
</td>
</tr>
<tr>
<td class="text-services">
<h3>Price Series Sample Sheet</h3>
<p>We record price of every product and seller in each tick.</p>
</td>
</tr>
<tr>
<td class="icon">
<img src="https://wx1.sinaimg.cn/mw690/b016a00egy1g97ze8uh04j20lb0bzjwx.jpg" alt="" style="width: 450px; max-width: 600px; height: auto; margin: auto; display: block;">
</td>
</tr>
<tr>
<td class="text-services">
<h3>Sold Item Statistics Sample Sheet</h3>
<p>We record sold items with product and seller information in each tick.</p>
</td>
</tr>
<tr>
<td class="icon">
<img src="https://wx2.sinaimg.cn/mw690/b016a00egy1g97ze8igs4j20lc0c0gnf.jpg" alt="" style="width: 450px; max-width: 600px; height: auto; margin: auto; display: block;">
</td>
</tr>
<tr>
<td class="text-services">
<h3>Sales Rank Sample Sheet</h3>
<p>We calculate sales rank in each tick .</p>
</td>
</tr>
<tr>
<td class="icon">
<img src="https://wx3.sinaimg.cn/mw690/b016a00egy1g97ze88f3wj20lb0bzdjf.jpg" alt="" style="width: 450px; max-width: 600px; height: auto; margin: auto; display: block;">
</td>
</tr>
<tr>
<td class="text-services">
<h3>Customer Purchase Sample Sheet</h3>
<p>We secretly record what items every customer purchases in each tick.</p>
</td>
</tr>
<tr>
<td class="icon">
<img src="https://wx1.sinaimg.cn/mw690/b016a00egy1g97ze7w1n5j20l40bvadi.jpg" alt="" style="width: 450px; max-width: 600px; height: auto; margin: auto; display: block;">
</td>
</tr>
<tr>
<td class="text-services">
<h3>Customer Wallet Sample Sheet</h3>
<p>We secretly record balance of all customers in each tick.</p>
</td>
</tr>
</table>
</td>
</tr>

</table>
<table >
<tr style="text-align:center;">
<td valign="top" width="50%" style="padding-top: 20px;" >
<p><a href="https://docs.google.com/spreadsheets/d/1DozTADVgqA7B_eu0TxOdnuo05m9BdQFoVaFdcgpSfW8/edit#gid=192419844" class="btn" style="border-radius: 30px; background:black ;color: #ffffff;">Click here to see more details!</a></p>
</td>
</tr>
</table>
</td>
</tr><!-- end: tr -->
<tr>
<td class="bg_white">
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
<tr>
<td class="bg_dark email-section" style="text-align:center;">
<div class="heading-section heading-section-white">
<span class="subheading">Author</span>
<h2>Group 6</h2>
<div style="color: #f1f1f1">Guo Mingyue A0198815M</div>
<div style="color: #f1f1f1">Wang Xinwei A0159419U</div>
<div style="color: #f1f1f1">Zhu Xiangqi  A0195470Y</div>
<p></p>
</div>
</td>
</tr><!-- end: tr -->
<tr>
</table>
</td>
</tr><!-- end:tr -->
</table>

</div>
</center>
</body>
</html>
'''
