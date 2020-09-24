package com.cloud.controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.cloud.domain.PageDto;
import com.cloud.domain.ProofBoardDto;
import com.cloud.service.ProofBoardService;

import io.swagger.annotations.ApiOperation;

@RestController
@RequestMapping("/proof")
public class ProofBoardController {

	@Autowired
	private ProofBoardService proofService;

	@ApiOperation(value = "인증된 게시글 가져오기(전체용)")
	@GetMapping(value = "/{campaign_no}/{page_no}")
	public ResponseEntity<Map<String, Object>> getProofList(@PathVariable("campaign_no") int campaignNo,
			@PathVariable("page_no") int pageNo) {
		Map<String, Object> map = new HashMap<>();
		PageDto page = new PageDto(pageNo, 5);
		page.setTotalCount(proofService.totalCount(campaignNo, true));
		List<ProofBoardDto> list = proofService.findAllByProof(campaignNo, true, page.getStartIndex(),
				page.getPerPageNum());

		map.put("list", list);
		map.put("page", page);

		return new ResponseEntity<Map<String, Object>>(map, HttpStatus.OK);
	}

	@ApiOperation(value = "인증 안 된 게시글 가져오기(관리자용)")
	@GetMapping(value = "/yet/{campaign_no}/{page_no}")
	public ResponseEntity<Map<String, Object>> getProofAdminList(@PathVariable("campaign_no") int campaignNo,
			@PathVariable("page_no") int pageNo) {
		Map<String, Object> map = new HashMap<>();
		PageDto page = new PageDto(pageNo, 5);
		page.setTotalCount(proofService.totalCount(campaignNo, false));
		List<ProofBoardDto> list = proofService.findAllByProof(campaignNo, false, page.getStartIndex(),
				page.getPerPageNum());

		map.put("list", list);
		map.put("page", page);

		return new ResponseEntity<Map<String, Object>>(map, HttpStatus.OK);
	}

	@ApiOperation(value = "인증 게시글 등록")
	@PostMapping(value = "/")
	public ResponseEntity<String> registProof(@RequestBody ProofBoardDto dto) {
		int res = proofService.insertProof(dto);
		if (res == 0) {
			return new ResponseEntity<String>("fail", HttpStatus.OK);
		}
		return new ResponseEntity<String>("success", HttpStatus.OK);
	}

	@ApiOperation(value = "인증 게시글 승인(관리자용)")
	@PatchMapping(value = "/{proof_no}")
	public ResponseEntity<String> passProof(@PathVariable("proof_no") int no) {
		int res = proofService.updateProof(no);
		if (res == 0) {
			return new ResponseEntity<String>("fail", HttpStatus.OK);
		}
		return new ResponseEntity<String>("success", HttpStatus.OK);
	}

	@ApiOperation(value = "공식 캠페인 오늘의 인증률")
	@GetMapping(value = "/official-percent/today/{campaign_no}")
	public ResponseEntity<Integer> getTodayOfiicial(@PathVariable("campaign_no") int no){
		int res = proofService.findTodayPassOfficial(no);
		return new ResponseEntity<Integer>(res, HttpStatus.OK);
	}
	
	@ApiOperation(value = "공식 캠페인 일주일 인증률")
	@GetMapping(value = "/official-percent/week/{campaign_no}")
	public ResponseEntity<Map<String, Object>> getWeekOfiicial(@PathVariable("campaign_no") int no){
		Map<String, Object> map = proofService.findWeekPassOfficial(no);
		if(map == null) {
			map = new HashMap<String, Object>();
			map.put("data", "데이터 없음");
		}
		return new ResponseEntity<Map<String, Object>>(map, HttpStatus.OK);
	}
	
}
