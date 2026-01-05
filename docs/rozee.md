# Rozee.pk Scraping Notes

## robots.txt Status: ALLOWED
* /job/ pages are allowed
* Rate limit: Wait 2 seconds between requests  
* User agent: Set to SkillScout

## HTML Structure

### Job List Container
* Tag: div
* Class: jlist float-left  
* ID: jobs

### Individual Job Card  
* Tag: div
* Class: job (sometimes "job active" for top job)

### Job Fields

#### Title
* Tag: h3  
* Class: s-18

#### Company  
* Tag: div
* Class: cname

#### Location
* Tag: div
* Class: jbody (also contains description)

## Example HTML (One Job Card)

```html
<div class="job ">
  <div class="jcont">
    <div class="jhead">
      <div class="jobt float-left">
        <h3 class="s-18" title="Python Developer">
          <a href="//www.rozee.pk/taaruff-pvt-ltd-python-developer-islamabad-jobs-1781618?utm_source=jobSearch&amp;utm_medium=website&amp;utm_content=jobSearch_1781618&amp;utm_campaign=ROZEE.PK_job_search">
            <bdi>Python Developer</bdi>
          </a>
        </h3>
        <div class="cname ">
          <bdi class="float-left">
            <a href="javascript:;" class="display-inline">Taaruff Pvt Ltd, </a>
            <a href="javascript:;" class="display-inline">Islamabad</a>
            <a href="javascript:;" class="display-inline">, Pakistan</a>
          </bdi>
        </div>
      </div>
    </div>
    <div class="clearfix"></div>
    <div class="jbody">
      <bdi>Location: Islamabad Pakistan
      Job Type: Full-time
      Experience Required: 5–7 Years
      Industry: Software Development, FinTech, AI,
      We are looking ..</bdi>
    </div>
  </div>
  <div class="jfooter">
    <div class="row">
      <div class="col-md-12 float-left">
        <span title="" data-toggle="tooltip" data-original-title="Posted On">
          <i class="calendar rz-calendar"></i>Dec 23, 2025
        </span>
        <span class="func-area uptos ">
          <i class="ex rz-func-area"></i>
          <span class="func-area-drn" title="" data-toggle="tooltip" data-original-title="Experience">5 Years</span>
        </span>
      </div>
      <div class="col-md-12 jcnt font16 ">
        <div class=" job-dtl clearfix">
          <div class="jblk">
            <div class="jcnt font16">
              <span class="label label-default float-left mr-2 font16 h42px br7 d-flex align-items-center ">MySQL</span>
              <span class="label label-default float-left mr-2 font16 h42px br7 d-flex align-items-center ">PostgreSQL</span>
              <span class="label label-default float-left mr-2 font16 h42px br7 d-flex align-items-center ">Django</span>
              <span class="label label-default float-left mr-2 font16 h42px br7 d-flex align-items-center ">Python Framework Command</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="clearfix"></div>
</div>
```