/**
 * @license Copyright (c) 2003-2018, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function (config) {
    // Define changes to default configuration here. For example:
    // config.language = 'fr';
    //config.uiColor = '#AADC6E';
    //config.disallowedContent = 'img{width,height};img[width,height]';
    config.allowedContent = true;
    //保证word导入格式
    config.pasteFromWordRemoveFontStyles = false;
    config.pasteFromWordRemoveStyles = false;
    //是否强制复制来的内容去除格式
    config.forcePasteAsPlainText =false; //不去除

    // 图片信息面板预览区内容的文字内容，默认显示CKEditor自带的内容
    config.image_previewText = '此处预览图片';
    //添加中文字体
    config.font_names = "宋体/SimSun;新宋体/NSimSun;仿宋_GB2312/FangSong_GB2312;楷体_GB2312/KaiTi_GB2312;黑体/SimHei;微软雅黑/Microsoft YaHei;幼圆/YouYuan;华文彩云/STCaiyun;华文行楷/STXingkai;方正舒体/FZShuTi;方正姚体/FZYaoti;" + config.font_names;

};

config.allowedContent = true;