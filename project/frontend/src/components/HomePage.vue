<template>
  <div>
    <h2>首页</h2>
    <!-- 上传大按钮模块 -->
    <div class="upload-button-module">
      <!-- 选择文件区域 -->
      <div class="upload-file-section" @click="openFileDialog('single')">
        <input
          type="file"
          ref="fileInputSingle"
          @change="handleFileChange('single')"
          multiple
          :accept="allowedFileTypes"
          style="display: none;"
        />
        <span>选择文件</span>
      </div>
      <!-- 选择文件夹区域 -->
      <div class="upload-folder-section" @click="openFileDialog('folder')">
        <input
          type="file"
          ref="fileInputFolder"
          @change="handleFileChange('folder')"
          multiple
          webkitdirectory
          directory
          style="display: none;"
        />
        <span>选择文件夹</span>
      </div>
    </div>
    <!-- 显示允许的文件类型 -->
    <p class="allowed-types">允许的文件类型: {{ allowedFileTypes.replace(/\./g, '').replace(/,/g, ', ') }}</p>
    <div v-if="selectedFiles.length > 0">
      <p>已选择文件: {{ selectedFiles.length === 1 ? selectedFiles[0].name : selectedFiles[0].name + ' 等 ' + selectedFiles.length + ' 个文件' }}</p>
      <button @click="showUploadConfirm">确认上传</button>
    </div>
    <div v-if="invalidFiles.length > 0" style="color: red;">
      以下文件类型不允许上传: {{ invalidFiles.join(', ') }}
    </div>
    <!-- 上传确认弹窗 -->
    <div v-if="showConfirmDialog" class="confirm-dialog">
      <div class="dialog-content">
        <p>确定要上传 {{ selectedFiles.length }} 个文件吗？</p>
        <button @click="uploadFiles">确定</button>
        <button @click="cancelUpload">取消</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
      selectedFiles: [],
      invalidFiles: [],
      uploadUrl: 'http://127.0.0.1:8000/api/upload/',
      allowedFileTypes: '.txt,.pdf,.doc,.docx,.csv,.jpg,.jpeg,.png,.wav,.mp3,.aac,.mp4',
      showConfirmDialog: false
    };
  },
  methods: {
    openFileDialog(type) {
      if (type === 'single') {
        this.$refs.fileInputSingle.click();
      } else {
        this.$refs.fileInputFolder.click();
      }
    },
    handleFileChange(type) {
      const inputRef = type === 'single' ? this.$refs.fileInputSingle : this.$refs.fileInputFolder;
      const files = inputRef.files;
      this.selectedFiles = [];
      this.invalidFiles = [];

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileExtension = file.name.split('.').pop().toLowerCase();
        if (this.allowedFileTypes.includes(`.${fileExtension}`)) {
          this.selectedFiles.push(file);
        } else {
          this.invalidFiles.push(file.name);
        }
      }
    },
    showUploadConfirm() {
      if (this.invalidFiles.length > 0) {
        console.error('存在不允许上传的文件类型，请重新选择。');
        return;
      }
      this.showConfirmDialog = true;
    },
    uploadFiles() {
      const formData = new FormData();
      this.selectedFiles.forEach((file) => {
        formData.append('files', file);
      });

      axios.post(this.uploadUrl, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then((response) => {
        console.log('文件上传成功:', response.data);
        this.selectedFiles = [];
        this.invalidFiles = [];
        this.$refs.fileInputSingle.value = '';
        this.$refs.fileInputFolder.value = '';
        this.showConfirmDialog = false;
      })
      .catch((error) => {
        console.error('文件上传失败:', error);
        this.showConfirmDialog = false;
      });
    },
    cancelUpload() {
      this.showConfirmDialog = false;
    }
  }
};
</script>

<style scoped>
.upload-button-module {
  display: flex;
  border: 1px solid #ccc;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  margin-bottom: 10px;
}

.upload-file-section,
.upload-folder-section {
  flex: 1;
  padding: 20px;
  text-align: center;
  transition: background-color 0.3s ease;
}

.upload-file-section:hover,
.upload-folder-section:hover {
  background-color: #f0f0f0;
}

.upload-file-section {
  border-right: 1px solid #ccc;
}

.allowed-types {
  margin-bottom: 20px;
}

.confirm-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}

button {
  margin: 5px;
}
</style>