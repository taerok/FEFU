<template>
  <div>
    <div class="section">
      <v-container>
        <v-row v-if="campaignType.id == 1" class="mb-8">

          <v-col cols="6" sm="8" lg="10">
            <h1 class="c-title text-left">
              {{ campaignType.name }}
            </h1>
          </v-col>

          <v-col v-if="isLoggedIn" cols="3" sm="2" lg="1">
            <router-link
              tag="button"
              class="c-btn c-primary"
              :to="{
                name: 'CampaignMake',
                params: { type: campaignType.id },
              }"
            >
              등록
            </router-link>
          </v-col>

          <v-col v-if="isLoggedIn" cols="3" sm="2" lg="1">
            <router-link
              tag="button"
              class="c-btn"
              :to="{
                name: 'CampaignTypeList',
                params: {
                  campaign_type: campaignType.id,
                  page_num: 1,
                },
              }"
            >
              더보기
            </router-link>
          </v-col>

          <v-col v-if="!isLoggedIn" cols="3" sm="2" lg="1" offset="3" offset-sm="2" offset-lg="1">
            <router-link
              tag="button"
              class="c-btn"
              :to="{
                name: 'CampaignTypeList',
                params: {
                  campaign_type: campaignType.id,
                  page_num: 1,
                },
              }"
            >
              더보기
            </router-link>
          </v-col>

        </v-row>
        <v-row v-else class="mb-8">

          <v-col cols="6" sm="8" lg="10">
            <h1 class="c-title text-left">
              {{ campaignType.name }}
            </h1>
          </v-col>

          <v-col cols="3" sm="2" lg="1" offset="3" offset-sm="2" offset-lg="1">
            <router-link
              tag="button"
              class="c-btn"
              :to="{
                name: 'CampaignTypeList',
                params: {
                  campaign_type: campaignType.id,
                  page_num: 1,
                },
              }"
            >
              더보기
            </router-link>
          </v-col>

        </v-row>

        <v-row>
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
      </v-container>
    </div>
  </div>
</template>

<script>
import CampaignCard from "../../components/campaign/CampaignCard.vue";
import { mapGetters } from 'vuex'

export default {
  props: {
    campaignType: Object,
    campaigninfo: Array,
  },
  components: {
    CampaignCard,
  },
  computed: {
      ...mapGetters('accounts', ['isLoggedIn'])
  }
};
</script>

<style lang="scss" scoped>
.c-txt {
  font-family: "S-CoreDream-7ExtraBold";
  font-size: 1rem;
}

.section {
  margin-top: 30px;
  margin-bottom: 100px;
  background: #fcfcfc;
}

.c-title {
  font-family: "NanumBarunpen";
}

.c-primary {
  background-color: var(--primary-color);
}

.c-btn {
  @extend .c-txt;
  width: 100%;
  height: 48px;

  border: 2px solid black;
  border-radius: 10px;
  text-align: center;

  &:focus {
    outline: none;
  }
}

.campaign-search {
  font-family: "NanumBarunpen";
  text-align: start;
  border: 2px solid black;
  border-radius: 10px;
  padding: 7px 10px;
  width: 100%;
  height: 48px;

  &:focus {
    outline: none;
  }
}

.c-select {
  border: 2px solid #000000;
}
</style>
