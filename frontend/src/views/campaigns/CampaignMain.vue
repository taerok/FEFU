<template>
  <v-container style="background: #fcfcfc">
    <!-- <v-container :class="[$vuetify.breakpoint.smAndDown ? '': 'mt-5']"> -->
    <v-tabs v-model="tab" centered grow color="#222">
      <v-tabs-slider color="#222"></v-tabs-slider>
      <v-tab
        v-for="item in items"
        :key="item.id"
        class="ml-0"
        style="background: #fcfcfc"
      >
        <span class="custom-tab">{{ item.name }}</span>
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item
        v-for="item in items"
        :key="item.id"
        style="background: #fcfcfc"
      >
        <CampaignList
          v-if="item.id == 1"
          :campaign-type="item"
          :campaigninfo="personalCampaignInfo"
        />
        <CampaignList
          v-if="item.id == 2"
          :campaign-type="item"
          :campaigninfo="companyCampaignInfo"
        />
        <CampaignList
          v-if="item.id == 3"
          :campaign-type="item"
          :campaigninfo="officialCampaignInfo"
        />
        <DailyQuest
          v-if="item.id == 4"
          :dailyQuestInfo="dailyQuestInfo"
          :isValid="isValid"
          :completed="completed"
        />
      </v-tab-item>
    </v-tabs-items>
    <!-- </v-container> -->
  </v-container>
</template>

<script>
import CampaignList from "./CampaignList.vue";
import DailyQuest from "./DailyQuest.vue";

import { mapGetters, mapActions } from "vuex";
import axios from "axios";
import SERVER from "@/api/api";

export default {
  components: {
    CampaignList,
    DailyQuest,
  },
  data() {
    return {
      slides: [
        {
          title: "100일 캠페인",
          content:
            "뜻을 함께하는 사람들과 함께, 100일 동안 함께하며 지구를 살리는 습관 만들기.",
          src: require("@/assets/images/nature-3.jpg"),
        },
        {
          title: "상시 캠페인",
          content:
            "오늘 당장 시작할 수 있는 기업캠페인과 공식 캠페인, 오늘 지구를 살리기 위한 당신의 실천은 무엇인가요?",
          src: require("@/assets/images/bg3.jpg"),
        },
        {
          title: "일일퀘스트",
          content:
            "일상 생활 속에서 쉽게 실천할 수 있는 12가지의 환경보호 생활 방안들, 지구를 살리는 한발자국",
          src: require("@/assets/images/bg7.jpg"),
        },
      ],
      tab: null,
      items: [
        { id: 1, name: "100일 캠페인" },
        { id: 2, name: "기업 캠페인" },
        { id: 3, name: "공식 캠페인" },
        { id: 4, name: "일일 퀘스트" },
      ],
      companyCampaignInfo: [],
      officialCampaignInfo: [],
      personalCampaignInfo: [],
      dailyQuestInfo: [],
      isValid: false,
      completed : [false, false, false, false, false, false, false, false, false, false, false, false],
    };
  },
  created() {
    this.getCompanyCampaignInfo("company", "", 1, "");
    this.getOfficialCampaignInfo("official", "", 1, "");
    this.getPersonalCampaignInfo("personal", "", 1, "");
    this.getDailyQuest();
  },
  computed: {
    ...mapGetters("accounts", ["config", "isLoggedIn"]),
  },
  methods: {
    ...mapActions("accounts", ["logout"]),
    getCompanyCampaignInfo(campaign_type, content, page_no, type) {
      axios
        .get(SERVER.URL + SERVER.ROUTES.campaigns.URL, {
          params: {
            campaign_type: campaign_type,
            content: content,
            page_no: page_no,
            type: type,
          },
        })
        .then((res) => (this.companyCampaignInfo = res.data.list.slice(0, 6)))
        .catch((err) => console.log(err.response));
    },
    getOfficialCampaignInfo(campaign_type, content, page_no, type) {
      axios
        .get(SERVER.URL + SERVER.ROUTES.campaigns.URL, {
          params: {
            campaign_type: campaign_type,
            content: content,
            page_no: page_no,
            type: type,
          },
        })
        .then((res) => (this.officialCampaignInfo = res.data.list.slice(0, 6)))
        .catch((err) => console.log(err.response));
    },
    getPersonalCampaignInfo(campaign_type, content, page_no, type) {
      axios
        .get(SERVER.URL + SERVER.ROUTES.campaigns.URL, {
          params: {
            campaign_type: campaign_type,
            content: content,
            page_no: page_no,
            type: type,
          },
        })
        .then((res) => (this.personalCampaignInfo = res.data.list.slice(0, 6)))
        .catch((err) => console.log(err.response));
    },
    getDailyQuest() {
      if (this.isLoggedIn) {
      // 현재는 단순히 일일퀘스트 정보만 가져오는데... 로그인한 경우 특정 유저의 details를 가져와야 됩니다.
      let configs = {
        headers: {
          Authorization: this.config,
        },
      };
      axios
        .get(SERVER.URL + SERVER.ROUTES.campaigns.dailyQuest, configs)
        .then((res) => {
          this.isValid = true;
          this.dailyQuestInfo = res.data;
          axios
            .get(SERVER.URL + SERVER.ROUTES.campaigns.dailyQuestDetail, configs)
            .then(response => {
              let completedDailyQuests = response.data
              for (let idx in completedDailyQuests) {
                this.completed[completedDailyQuests[idx].no - 1] = true
              }
            })
        })
        .catch((err) => {
          if (err.response.status == 401) {
            alert('로그인 정보가 만료되었습니다!');
            this.logout();
          }
          this.isValid = false;
        });
      }
    },
    goCampaignDetail() {
      this.$router.push({
        name: "CampaignDetailInfo",
        params: { CampaignNo: 1 },
      });
    },
    goCompanyCampaignList() {
      this.$router.push({ name: "CompanyCampaignList" });
    },
  },
};
</script>

<style scoped>
h2 {
  margin-top: 20px;
  margin-bottom: 20px;
}

.custom-tab {
  font-family: "S-CoreDream-7ExtraBold";
}
</style>
