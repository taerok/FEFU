<template>
  <div>
    <v-img
      class="campaign-header-img"
      height="200px"
      :src="
        campaign.photo
          ? imageSrc(campaign.photo)
          : '@/assets/images/lazy-loading.jpg'
      "
      lazy-src="@/assets/images/lazy-loading.jpg"
    >
      <template v-slot:placeholder>
        <lazy-loading />
      </template>
    </v-img>

    <div v-if="campaign">
      <v-list class="custom-list">
        <v-list-item
          v-for="(item, index) in items"
          :key="index"
          no-action
          class="custom-list-item"
          :class="`custom-list-item-${
            listColorName[index % listColorName.length]
          }`"
          :to="{ name: item.link, params: { campaignNo: campaign.no } }"
        >
          <v-list-item-content>
            <v-list-item-title v-text="item.name"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </div>
  </div>
</template>

<script>
import SERVER from "@/api/api";

export default {
  props: ["campaign"],
  data() {
    return {
      listColorName: [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "purple",
      ],
      items: [
        { name: "캠페인소개", link: "CampaignDetailInfo" },
        { name: "인증현황", link: "CampaignDetailCertifi" },
        { name: "인증게시판", link: "CampaignDetailPostings" },
      ],
    };
  },
  methods: {
    imageSrc(filename) {
      return SERVER.IMAGE_URL + filename;
    },
  },
};
</script>

<style lang="scss" scoped>
.campaign-header-img {
  border: 2px solid black;
  border-radius: 15px;
}

.capmaign-info {
  font-family: "NanumBarunpen";
}

.custom-list {
  margin-top: 20px;
  font-family: "S-CoreDream-7ExtraBold";
}

.campaign-info-list {
  font-family: "S-CoreDream-7ExtraBold";
  border: 2px solid black;
  border-radius: 10px;
  padding: 5px 0;
}

.custom-list-item {
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
