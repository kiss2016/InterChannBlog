KindEditor.ready(function (k) {
        k.create('textarea[name=content]',{
        resizeType:2, //2时可以拖动改变宽度和高度，1时只能改变高度，0时不能拖动
        allowFileManager: false, //是否允许浏览服务器已上传文件
        allowImageManager: true,
        allowPreviewEmoticons : false,
        pasteType: 1, //设置粘贴类型，0：禁止粘贴，1：纯文本粘贴，2：HTML粘贴
//        allowImageRemote : false,
        uploadJson : '/uploads/images',
        width:'800px',
        height:'600px',
    });
});