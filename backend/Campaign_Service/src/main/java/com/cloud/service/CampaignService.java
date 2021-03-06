package com.cloud.service;

import java.util.List;
import java.util.Map;

import com.cloud.domain.CampaignDto;

public interface CampaignService {

	public List<CampaignDto> findAll(String campaignType, int pageNo, String type, String content, int startIndex, int perPageNum);
	public List<CampaignDto> findByJoinCampaign(String username);
	public List<CampaignDto> findByRegistCampaign(String username);
	public List<String> findTagByNo(int no);
	public Map<String, Object> findDetail(int no);
	public int findByCount(String campaignType, int pageNo, String type, String content);
	public int insertCampaign(Map<String, Object> data);
	public int updateCampaign(CampaignDto dto);
	public int deleteCampaign(int no);
	public int checkJoin(int no, String username);
	public int joinCampaign(int no, String username);
	public int leaveCampaign(int no, String username);
}
