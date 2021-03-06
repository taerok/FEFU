<template>
  <div>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on, attrs }">
        <button class="custom-make-btn" v-bind="attrs" v-on="on">
          인증글 작성
        </button>
      </template>
      <v-card style="border: 3px solid #000000">
        <v-card-title
          style="
            background-color: var(--primary-color);
            border-bottom: 2px solid #000000;
          "
        >
          <span class="headline">인증글 작성</span>
        </v-card-title>
        <v-card-text class="py-0">
          <v-form ref="form">
            <v-container class="pb-0">
              <v-row>
                <v-col cols="12" class="py-0">
                  <v-img
                    @click="onClickImageUpload"
                    id="Preview_image_create"
                    height="230px"
                    :style="
                      !url ? 'border-bottom: 1px solid rgba(0, 0, 0, 0.42)' : ''
                    "
                    :src="!!url ? url : require('@/assets/images/noimage.jpg')"
                    lazy-src="@/assets/images/lazy-loading.jpg"
                  >
                    <template v-slot:placeholder>
                      <lazy-loading />
                    </template>
                  </v-img>
                  <v-file-input
                    class="mt-5"
                    label="오늘의 미션 인증 사진"
                    ref="imageInput"
                    v-model="images"
                    :rules="imageRules"
                    filled
                    prepend-icon=""
                    append-icon="mdi-camera"
                    color="#37cdc2"
                    accept="image/*"
                    @change="Preview_image"
                  ></v-file-input>
                </v-col>

                <v-col cols="12" class="py-0">
                  <v-text-field
                    v-model="proofPost.title"
                    label="인증글 제목"
                    name="인증글 제목"
                    type="text"
                    required
                    filled
                    autofocus
                    :rules="[(v) => !!v || '제목을 적어주세요']"
                    autocapitalize="off"
                    autocorrect="off"
                    autocomplete="off"
                    color="#37cdc2"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" class="py-0">
                  <v-textarea
                    v-model="proofPost.content"
                    label="내용"
                    name="내용"
                    type="text"
                    required
                    filled
                    :rules="[(v) => !!v || '내용을 적어주세요']"
                    autocapitalize="off"
                    autocorrect="off"
                    autocomplete="off"
                    color="#37cdc2"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>
        <v-card-actions class="px-5">
          <v-spacer></v-spacer>
          <v-btn class="c-btn" text @click="dialog = false"> 취소 </v-btn>
          <v-btn class="c-btn" text @click="registProof"> 등록 </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";
import SERVER from "@/api/api";
import router from "@/router";
import { mapGetters } from "vuex";
import { mixinUploadImage } from "@/components/mixin/mixinUploadImage";

export default {
  props: ["campaign"],
  mixins: [mixinUploadImage],
  data() {
    return {
      url: null,
      images: null,
      imageRules: [(v) => !!v || "이미지를 첨부해주세요"],
      proofPost: {
        campaignNo: 0,
        title: "",
        content: "",
        photo: "",
        writer: "",
      },
      user: null,
      dialog: false,
    };
  },
  computed: {
    ...mapGetters("accounts", ["config", "USERNAME"]),
  },
  methods: {
    onClickImageUpload() {
      this.$refs.imageInput.$refs.input.click()
    },
    Preview_image() {
      if (!this.images) {
        this.url = null;
      } else {
        this.url = URL.createObjectURL(this.images);
      }
      this.preUploadImage();
    },
    preUploadImage() {
      this.uploadImage(this.images)
        .then((res) => {
          this.proofPost.photo = res.data.fileName;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async registProof() {
      if (!this.$refs.form.validate()) {
        return;
      }

      this.proofPost.campaignNo = this.campaign.no;
      this.proofPost.writer = this.USERNAME;

      await axios
        .post(
          SERVER.URL + SERVER.ROUTES.campaigns.URL + "/proof/",
          this.proofPost,
          {
            headers: {
              Authorization: this.config,
            },
          }
        )
        .then(() => {
          alert("인증글이 등록되었어요");
          this.dialog = false;
          router
            .push({
              name: "CampaignDetailInfo",
              params: { campaginNo: this.proofPost.campaignNo },
            })
            .catch((error) => {
              if (error.name === "NavigationDuplicated") {
                location.reload();
              }
            });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.custom-make-btn {
  font-family: "S-CoreDream-7ExtraBold";
  font-size: 1rem;
  width: 100%;
  height: 48px;
  margin-top: 20px;
  background-color: var(--primary-color);
  border: 2px solid black;
  border-radius: 10px;
  text-align: center;
}

.c-btn {
  font-family: "S-CoreDream-7ExtraBold";
  border: 2px solid black;
  border-radius: 10px;
}

#Preview_image_create {
  cursor: pointer;
}
</style>
