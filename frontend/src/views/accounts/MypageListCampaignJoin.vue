<template>
  <div>
    <v-container justify="start">
      <div class="c-title c-card__content">참여 캠페인</div>

      <div class="c-txt c-card__content d-flex flex-column">
        <v-row v-if="campaigninfo.length != 0">
          <v-col
            cols="12"
            sm="6"
            md="4"
            v-for="(campaign, idx) in campaigninfo"
            :key="idx"
            align="center"
          >
            <CampaignCard
              :campaign="campaign"
              :to="{
                name: 'CampaignDetailInfo',
                params: { campaignNo: campaign.no },
              }"
            />
          </v-col>
        </v-row>
        <core-banner
          v-else
          content="참여한 캠페인이 없네요. 캠페인참여해봐요!🌎"
          btn-text="참여하러 가기"
          color="#fcfcfc"
          align="center"
          :to="{ name: 'CampaignMain' }"
        />
      </div>
    </v-container>
  </div>
</template>

<script>
import SERVER from "@/api/api";
import axios from "axios";

import { mixinGetUserInfo } from "@/components/mixin/mixinGetUserInfo";

import { mapGetters } from "vuex";

import CampaignCard from "@/components/campaign/CampaignCard.vue";
import CoreBanner from "@/components/core/Banner.vue";

export default {
  name: "MypageListCampaignJoin",
  mixins: [mixinGetUserInfo],
  components: { CampaignCard, CoreBanner },
  data() {
    return {
      isJoined: false,
      listColorName: [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "purple",
      ],
      userinfo: {
        no: 0,
        username: "",
        password: null,
        nickname: "",
        age: 0,
        gender: "남자",
        ecoPoint: 0,
        exp: 0,
        profileImage: "",
      },
      campaigninfo: [],
    };
  },
  created() {
    this.getUserInfo().catch((err) => console.log(err));
    this.getCampaignJoin();
  },
  computed: {
    ...mapGetters("accounts", ["config", "USERNAME"]),
  },
  methods: {
    imageSrc(filename) {
      return SERVER.IMAGE_URL + filename;
    },
    getCampaignJoin() {
      let configs = {
        headers: {
          Authorization: this.config,
        },
      };
      axios
        .get(SERVER.URL + SERVER.ROUTES.campaigns.join, configs)
        .then((res) => {
          this.campaigninfo = res.data;
        })
        .catch((err) => {
          console.log(err.response);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.c-sidebar {
  border: 2px solid black;
  border-radius: 10px;
  &__img {
    border-radius: 50%;
  }
  &__name {
    font-size: 1rem;
    width: 100%;
    height: 48px;
  }
}

.c-card__content {
  border: 2px solid black;
  border-radius: 5px;
  padding: 10px 20px;
  margin: 10px 0;
}
.c-txt,
.c-title {
  font-family: "NanumBarunpen";
}

.c-title {
  text-align: start;
  font-size: 1.5rem;
}

.c-btn {
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

.c-list {
  margin-top: 20px;
  font-family: "S-CoreDream-7ExtraBold";
}

.c-list-item {
  border: 2px solid black;
  &:first-child {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }
  &:last-child {
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }

  &:not(:last-child) {
    // border-bottom: 2px solid black;
    margin-bottom: -2px;
  }

  &-red.v-list-group--active,
  &-red:hover {
    background: #cf6a87;
  }

  &-orange.v-list-group--active,
  &-orange:hover {
    background: #f19066;
  }

  &-yellow.v-list-group--active,
  &-yellow:hover {
    background: #fdcb6e;
  }

  &-green.v-list-group--active,
  &-green:hover {
    background: #b8e994;
  }

  &-blue.v-list-group--active,
  &-blue:hover {
    background: #82ccdd;
  }

  &-indigo.v-list-group--active,
  &-indigo:hover {
    background: #60a3bc;
  }

  &-purple.v-list-group--active,
  &-purple:hover {
    background: #786fa6;
  }
}
</style>
