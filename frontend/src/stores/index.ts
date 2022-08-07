import { defineStore } from 'pinia'
import { toRaw } from 'vue';

const trim = str => str.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
const generate_uuid = () => {
  let s4 = () => (((1+Math.random()) * 0x10000) | 0).toString(16).substring(1);
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4()+s4()+s4()
}

export const useMainStore = defineStore('main', {
  // 类似于组件的 data, 用来储存全局状态的
  state: () => {
    return {
      scaleRatio: 1,
      imgWidthLimit: 0,
      imgHeightLimit: 0,
      mouseActLatestX: 0,
      mouseActLatestY: 0,
      sideBarExpanded: false,
      sideBarExpandedDone: false,
      sideBarExpandedPtr: null,
      styleSolution: null,
      currentImage: "",
      sideBarLocked: false,
      wsUUID: generate_uuid(),
      wsBroken: false,
      ready: null,
      mainStruct: {
        // '1.jpg': {
          // img
          // realName
        //   pouch: [
        //     {
        //       img: '1.jpg',
        //       id: "0",
        //       category: 'src',
        //       focus: true,
        //       text: "こんにちは。今日もいい天気ですね",
        //       removing: false,
        //       removingProtect: false,
        //       carry: {
        //         loading: false,
        //         dicthtml: ''
        //       }
        //     },
        //     {
        //       img: '1.jpg',
        //       id: "1",
        //       category: 'dst',
        //       focus: false,
        //       text: "你好。今天天气真不错你好。",
        //       removing: false,
        //       removingProtect: false,
        //       carry: {
        //         translator: '腾讯翻译'
        //       }
        //     },
        //     {
        //       img: '1.jpg',
        //       id: "2",
        //       category: 'dst',
        //       focus: false,
        //       text: "你好。今天天气真不错你好。",
        //       removing: false,
        //       removingProtect: false,
        //       carry: {
        //         translator: '腾讯翻译'
        //       }
        //     },
        //     {
        //       img: '1.jpg',
        //       id: "3",
        //       category: 'dst',
        //       focus: true,
        //       removing: false,
        //       removingProtect: false,
        //       text: "你好。今天天气真不错你好。你好。今天天气真不错你好。你好。今天天气真不错你好。你好。今天天气真不错你好。你好。今天天气真不错你好。你好。今天天气真不错你好。你好。今天天气真不错你好。",
        //       carry: {
        //         translator: '百度翻译'
        //       }
        //     },
        //   ],
        //   reverseIndex: {
        //     // '0': 0,
        //     // '1': 1,
        //     // '2': 2,
        //     // '3': 3,
        //   },
        //   textBoxes: [
        //     {
        //       id: 'md5',
        //       text: "空调坏了的罗德岛",
        //     },
        //     {
        //       id: 'md6',
        //       text: "简直热死了",
        //     }
        //   ]
        // }
      },
      windows: {
        settings: {
          preclose: false,
          show: false,
          locked: false,
        },
        files: {
          preclose: false,
          show: false,
          locked: false,
        }
      },
      myStyles: {
        '微软黑粗': {
          border: false,
          borderw: 3.6,
          borderc: '#ff0000',
          color: "#202020",
          font: "微软雅黑",
          fontsize: 36,
          lns: 5,
          lts: 1,
          name: "微软黑粗",
          order: 0,
          weight: 700,
          select: false,
        }
      },
      defaultTextStyle: {
        name: "微软黑粗",
        border: false,
        borderw: 3.6,
        borderc: '#ff0000',
        color: "#202020",
        font: "微软雅黑",
        fontsize: 36,
        lns: 5,
        lts: 1,
        weight: 700,
      },
      settings: {
        global: {
          idx: 0,
          focus: true,
          label: '全局选项',
          icon: 'avatar'
        },
        fonts: {
          idx: 1,
          focus: false,
          label: '字体配置',
          icon: 'star'
        }
      },
    }
  },
  // 类似于组件的 computed, 用来封装计算属性，有缓存的功能
  getters: {
    dropdownHeight() {
      return Object.entries(JSON.parse(JSON.stringify(this.myStyles))).length * 48 + 16
    },
    myStylesOrdered() {
      let arr = []
      for (let [key, val] of Object.entries(this.myStyles)) {
        arr.push(val)
      }
      return arr.sort((x,y)=>{0+(x.order-y.order)})
    }
  },
  // 类似于组件的 methods, 用来封装业务逻辑，修改state
  actions: {
    switchReadyStatus(status){
      this.ready = status
    },
    switchFocus(img: String, id: String, status: Boolean){
      let copied = JSON.parse(JSON.stringify(this.mainStruct))
      for (let [key, value] of Object.entries(copied)) {
        let item_idx = 0;
        for (let item of value.pouch) {
          if (item.focus == true) {
            this.mainStruct[key].pouch[item_idx].focus = false;
          }
          item_idx+=1;
        }
      }
      if (status == true) {
        for (let [key, value] of Object.entries(copied)) {
          if (key == img) {
            let item_idx = 0;
            for (let item of value.pouch) {
              if (item.id == id) {
                this.mainStruct[img].pouch[item_idx].focus = true;
                return;
              }
              item_idx += 1;
            }
          }
        }
      }
    },
    expandSideBar(status: bool) {
      if (status) {
        this.sideBarExpanded = status
        if (this.sideBarExpandedPtr===null) {
          this.sideBarExpandedPtr = window.setTimeout(()=>{
            this.sideBarExpandedDone = true;
            this.sideBarExpandedPtr = null
          }, 200)
        }
      } else {
        if (this.sideBarLocked) {return}
        this.sideBarExpanded = status
        if (this.sideBarExpandedPtr!==null) {
          window.clearTimeout(this.sideBarExpandedPtr)
          this.sideBarExpandedPtr=null
          this.sideBarExpandedDone = false;
        } else {
          this.sideBarExpandedDone = false;
        }
      }
    },
    updatePouchText(img:String, id:String, newText:String){
      let fileProxy = null
      for (let [key, value] of Object.entries(this.mainStruct)) {
        if (key == img) {
          fileProxy = value;
          break;
        }
      }
      if (fileProxy === null) {
        return false
      }
      let textIndex = fileProxy.reverseIndex[id]
      if (textIndex === undefined) {
        return false
      }
      if (newText.length == 0) {
        // 执行删除逻辑
        this.delayRemove(img, id)
      } else if (fileProxy.pouch[textIndex].category =='dst') {
        if (newText.indexOf('\n\n')<0) {
          // 更新内容
          fileProxy.pouch[textIndex].text = trim(newText)
        } else{
          // 切分组件
          fileProxy.pouch[textIndex].removing=true
          if (!fileProxy.pouch[textIndex].removingProtect) {
            fileProxy.pouch[textIndex].removingProtect=true
            window.setTimeout(() => {
              this.removeItem(img, id)
            }, 300)
            window.setTimeout(() => {
              this.appendItems(img, newText.split('\n\n').map(trim).filter(x=>x.length>0), 'dst')
            }, 350)
            return true
          }
        }
      } else {
        // src不允许拆分
        fileProxy.pouch[textIndex].text = newText.replace(/\n/g, '');
      }
      return false
    },
    activateWindow(winname: String, action: String) {
      if (this.windows[winname].lockded) {
        return
      }
      if (action == 'close') {
        document.body.style.overflowY=''; // 组件里还有一层取消
        this.windows[winname].show=false
      } else {
        document.body.style.overflowY='hidden';
        this.windows[winname].show=true
      }
    },
    lockWindow(winname: String, action: Boolean) {
      this.windows[winname].locked = action
    },
    removeItem(img: String, id: String) {
      let fileProxy = null
      for (let [key, value] of Object.entries(this.mainStruct)) {
        if (key == img) {
          fileProxy = value;
          break;
        }
      }
      if (fileProxy === null) {
        return
      }
      let idx = fileProxy.reverseIndex[id]
      fileProxy.pouch.splice(idx, 1)
      let flag1 = false
      for (let [key, value] of Object.entries(fileProxy.reverseIndex)) {
        if (value > idx) {
          fileProxy.reverseIndex[key] -= 1
        }
      }
      delete fileProxy.reverseIndex[id]
    },
    updateScaleRatio(newRatio: Number) {
      this.scaleRatio = newRatio
    },
    updateImageSizeLimit(newWidth: Number, newHeight: Number) {
      this.imgWidthLimit = newWidth;
      this.imgHeightLimit = newHeight;
      // 每次响应图片的时候都会刷新图片大小信息，所以不能直接设置响应时清空，因为响应不等于换图
      this.mouseActLatestX = Math.min(Math.max(0, this.mouseActLatestX), this.imgWidthLimit)
      this.mouseActLatestY = Math.min(Math.max(0, this.mouseActLatestY), this.imgHeightLimit)
    },
    switchStyle(name: String){
      let copied = JSON.parse(JSON.stringify(this.myStyles))
      for (let [key, value] of Object.entries(copied)) {
        this.myStyles[key].select = false
      }
      this.myStyles[name].select = true;
      this.styleSolution = name
    },
    delayRemove(img: String, tid: String) {
      let fileProxy = null
      for (let [key, value] of Object.entries(this.mainStruct)) {
        if (key == img) {
          fileProxy = value;
          break;
        }
      }
      if (fileProxy === null) {
        return { remove: false, carry: null }
      }
      let textIndex = fileProxy.reverseIndex[tid]
      fileProxy.pouch[textIndex].removing=true
      if (!fileProxy.pouch[textIndex].removingProtect) {
        fileProxy.pouch[textIndex].removingProtect=true
        window.setTimeout(() => {
          this.removeItem(img, tid)
        }, 300)
      }
    },
    appendItems(img:String, items: string[], category: String) {
      // search max id
      let fileProxy = null
      for (let [key, value] of Object.entries(this.mainStruct)) {
        if (key == img) {
          fileProxy = value;
          break;
        }
      }
      if (fileProxy === null) {
        return false
      }
      let newid = -1
      for (let [key, value] of Object.entries(fileProxy.reverseIndex)) {
        if (parseInt(key) > newid) {
          newid = parseInt(key);
        }
      }
      newid += 1;
      for (let text of items) {
        fileProxy.pouch.push({
          img: img,
          id: newid.toString(),
          category: category,
          focus: true,
          removing: false,
          removingProtect: false,
          text: text,
          carry: category=='dst'?{
            translator: '',
            translatorColor: '',
          }:{
            loading: false,
            dicthtml: ""
          }
        })
        fileProxy.reverseIndex[newid.toString()] = fileProxy.pouch.length - 1;
        newid += 1
      }
    },
    switchSideBarLock(){
      this.sideBarLocked = !this.sideBarLocked
    },
    switchSettingFocus(idx: Number){
      let jdx = 0;
      for (let [key, value] of Object.entries(this.settings)) {
        if (jdx == idx) {
          value.focus = true
        } else {
          value.focus = false
        }
        jdx += 1;
      }
    },
    appendTextBox(img: String, text: String, style: String) {
      let fileProxy = null
      for (let [key, value] of Object.entries(this.mainStruct)) {
        if (key == img) {
          fileProxy = value;
          break;
        }
      }
      if (fileProxy === null) {
        return { success: false, carry: null }
      }
      // estimate textbox size
      let t = Math.sqrt(text.length)
      let rowlength = Math.ceil(t+1) 
      let rownum = Math.floor(t)
      let styleinfo = this.myStyles.hasOwnProperty(this.styleSolution)?this.myStyles[this.styleSolution]:this.defaultTextStyle
      // 特指竖排文字
      let est_height = rowlength * styleinfo.fontsize +  (rowlength-1)*styleinfo.lts + 3*2
      let est_width = rownum * styleinfo.fontsize +  (rowlength-1)*styleinfo.lns + 4*2
      let uuid = generate_uuid()
      fileProxy.textBoxes[uuid] = {
        img: img,
        id: uuid,
        text: text,
        style: style,
        height: est_height + Math.floor(styleinfo.fontsize/2),
        translate_x: parseFloat(Math.min(Math.max(0, this.mouseActLatestX - est_width/2), this.imgWidthLimit-5).toFixed(1)),
        translate_y: parseFloat(Math.min(Math.max(0, this.mouseActLatestY - est_height/2), this.imgHeightLimit-5).toFixed(1)),
      }
    },
    removeTextBox(img: String, tbid: String) {
      let tbProxy = this.mainStruct[img].textBoxes
      if (tbProxy == undefined) {
        return { remove: false, carry: null }
      } 
      delete tbProxy[tbid]
      return { remove: true, carry: null }
    },
    updateTextBoxPos(img: String, tbid: String, tx: Number, ty: Number) {
      try {
        this.mainStruct[img].textBoxes[tbid].translate_x = tx
        this.mainStruct[img].textBoxes[tbid].translate_y = ty
      } catch {}
    },
    updateTextBoxHeight(img: String, tbid: String, height: number) {
      try {
        this.mainStruct[img].textBoxes[tbid].height = height
      } catch {}
    },
    backendImageUpdate(imgLst: Array) {
      let md5_array = [];
      for (let [imgMD5, imgName] of imgLst) {
        md5_array.push(imgMD5);
        if (this.mainStruct.hasOwnProperty(imgMD5)) {
          continue
        } // else 
        this.mainStruct[imgMD5] = {
          img: imgMD5,
          realName: imgName,
          pouch: [],
          reverseIndex: {},
          textBoxes: {},
        }
      }
      // 清理多余的图片
      let removes = []
      for (let md5 of Object.keys(this.mainStruct)) {
        if (md5_array.indexOf(md5) < 0) {
          removes.push(md5)
        }
      }
      for (let md5 of removes) {
        delete this.mainStruct[md5]
      }
      if (imgLst.length == 0) {
        this.switchMainFrameImg("")
      }
    },
    switchWindowPreclose(winname:String, status:Boolean) {
      this.windows[winname].preclose = status
    },
    switchMainFrameImg(md5: String) {
      this.currentImage = md5
    },
    wsClosed() {
      this.wsBroken = true
    },
    appendSrcDstText(imgMD5: String, text: String, carry: Object, text_type: String) {
      let fileProxy = null
      for (let [key, value] of Object.entries(this.mainStruct)) {
        if (key == imgMD5) {
          fileProxy = value;
          break;
        }
      }
      if (fileProxy === null) {
        return false
      }
      // 查找目前最大标记位
      let newid = -1
      for (let [key, value] of Object.entries(fileProxy.reverseIndex)) {
        if (parseInt(key) > newid) {
          newid = parseInt(key);
        }
      }
      newid += 1;
      fileProxy.pouch.push({
        img: imgMD5,
        id: newid.toString(),
        category: text_type,
        focus: true,
        text: text,
        removing: false,
        removingProtect: false,
        carry: carry
      })
      fileProxy.reverseIndex[newid.toString()] = fileProxy.pouch.length - 1
    },
    updateStyle(data) {
      if (data.name == '') {console.log('style name empty');return}
      let order = -1
      let updated = false
      for (let [key, val] of Object.entries(this.myStyles)) {
        if (key == data.name) {
          val.name = data.name 
          val.font = data.font 
          val.fontsize = data.fontsize 
          val.color = data.color
          val.lts = data.lts 
          val.lns = data.lns 
          val.weight = data.weight 
          val.border = data.border 
          val.borderw = data.borderw 
          val.borderc = data.borderc
          updated = true
        }
        order = Math.max(order, val.order)
      }
      order += 1
      if (!updated) {
        // append
        let data_c = JSON.parse(JSON.stringify(data))
        data_c.order = order
        this.myStyles[data.name] = data_c
      }
    },
    upliftStyle(name: String) {
      let ptr = this.myStyles[name]
      if (ptr == undefined) {
        console.log('uplift error'); return
      }
      delete this.myStyles[name]
      this.updateStyle(ptr)
      this.myStyles[name].order = -1
      for (let [key, val] of Object.entries(this.myStyles)) {
        val.order = val.order + 1
      }
    },
    deleteStyle(name:String) {
     try {
       delete this.myStyles[name]
     } catch {}
    },
    updateLastRequestPos(ox, oy) {
      this.mouseActLatestX = Math.min(Math.max(ox, 0),this.imgWidthLimit)
      this.mouseActLatestY = Math.min(Math.max(oy, 0),this.imgHeightLimit)
    },
    searchImgRealFileName(img: String) {
      let ptr = undefined
      try {
        ptr = this.mainStruct[img]
      } catch {

      }
      if (ptr != undefined) {
        let name = ptr.realName 
        if (name.indexOf('.') >= 0) {
          // 有扩展名
          name = name.substring(0, name.lastIndexOf('.'))
        }
        if (name == undefined || name == "") {
          name = 'download'
        }
        return name 
      }
      return 'download'
    },
    updateWordExplain(img: String, html: String, iid: String){
      try {
        let carryProxy = this.mainStruct[img].pouch[this.mainStruct[img].reverseIndex[iid]].carry
        carryProxy.dicthtml = html
        carryProxy.loading = false
      } catch {
        console.log('word explaination update error')
      }
    },
    requestWordTranslate(img: String, iid: String) {
      try {
        this.mainStruct[img].pouch[this.mainStruct[img].reverseIndex[iid]].carry.loading = true
      } catch {
        console.log('word explaination loading status update error')
      }
    }
  },
})