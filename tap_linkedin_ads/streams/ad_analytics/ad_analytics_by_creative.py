"""Stream type classes for tap-linkedin-ads."""

from __future__ import annotations

import typing as t
from datetime import timezone
from importlib import resources

import pendulum
from singer_sdk.typing import (
    IntegerType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
)

from tap_linkedin_ads.streams.ad_analytics.ad_analytics_base import AdAnalyticsBase
from tap_linkedin_ads.streams.streams import CreativesStream

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

SCHEMAS_DIR = resources.files(__package__) / "schemas"
UTC = timezone.utc


class _AdAnalyticsByCreativeInit(AdAnalyticsBase):
    name = "AdAnalyticsByCreativeInit"
    parent_stream_type = CreativesStream

    schema = PropertiesList(
        Property("landingPageClicks", IntegerType),
        Property("reactions", IntegerType),
        Property("adUnitClicks", IntegerType),
        Property("creative_id", StringType),
        Property("documentCompletions", IntegerType),
        Property("documentFirstQuartileCompletions", IntegerType),
        Property("clicks", IntegerType),
        Property("documentMidpointCompletions", IntegerType),
        Property("documentThirdQuartileCompletions", IntegerType),
        Property("downloadClicks", IntegerType),
        Property("jobApplications", StringType),
        Property("jobApplyClicks", StringType),
        Property("postViewJobApplications", StringType),
        Property("costInUsd", StringType),
        Property("postViewRegistrations", StringType),
        Property("registrations", StringType),
        Property("talentLeads", IntegerType),
        Property("viralDocumentCompletions", IntegerType),
        Property("viralDocumentFirstQuartileCompletions", IntegerType),
        Property("viralDocumentMidpointCompletions", IntegerType),
        Property("viralDocumentThirdQuartileCompletions", IntegerType),
        Property("viralDownloadClicks", IntegerType),
        Property("viralJobApplications", StringType),
        Property("viralJobApplyClicks", StringType),
        Property("costInLocalCurrency", StringType),
        Property("viralRegistrations", IntegerType),
        Property("approximateUniqueImpressions", IntegerType),
        Property("cardClicks", IntegerType),
        Property("cardImpressions", IntegerType),
        Property("commentLikes", IntegerType),
        Property("viralCardClicks", IntegerType),
        Property("viralCardImpressions", IntegerType),
        Property("viralCommentLikes", IntegerType),
        Property("actionClicks", IntegerType),
        Property("comments", IntegerType),
        Property("companyPageClicks", IntegerType),
        Property("conversionValueInLocalCurrency", StringType),
        Property(
            "dateRange",
            ObjectType(
                Property(
                    "end",
                    ObjectType(
                        Property("day", IntegerType),
                        Property("month", IntegerType),
                        Property("year", IntegerType),
                        additional_properties=False,
                    ),
                ),
                Property(
                    "start",
                    ObjectType(
                        Property("day", IntegerType),
                        Property("month", IntegerType),
                        Property("year", IntegerType),
                        additional_properties=False,
                    ),
                ),
            ),
        ),
        Property("day", StringType),
        Property("externalWebsiteConversions", IntegerType),
        Property("externalWebsitePostClickConversions", IntegerType),
        Property("externalWebsitePostViewConversions", IntegerType),
        Property("follows", IntegerType),
        Property("fullScreenPlays", IntegerType),
        Property("impressions", IntegerType),
        Property("landingPageClicks", IntegerType),
        Property("leadGenerationMailContactInfoShares", IntegerType),
        Property("leadGenerationMailInterestedClicks", IntegerType),
        Property("likes", IntegerType),
        Property("oneClickLeadFormOpens", IntegerType),
        Property("oneClickLeads", IntegerType),
        Property("opens", IntegerType),
        Property("otherEngagements", IntegerType),
        Property("sends", IntegerType),
        Property("shares", IntegerType),
        Property("textUrlClicks", IntegerType),
        Property("totalEngagements", IntegerType),
        Property("videoCompletions", IntegerType),
        Property("videoFirstQuartileCompletions", IntegerType),
        Property("videoMidpointCompletions", IntegerType),
        Property("videoStarts", IntegerType),
        Property("videoThirdQuartileCompletions", IntegerType),
        Property("videoViews", IntegerType),
        Property("viralClicks", IntegerType),
        Property("viralComments", IntegerType),
        Property("viralCompanyPageClicks", IntegerType),
        Property("viralExternalWebsiteConversions", IntegerType),
        Property("viralExternalWebsitePostClickConversions", IntegerType),
        Property("viralExternalWebsitePostViewConversions", IntegerType),
        Property("viralFollows", IntegerType),
        Property("viralFullScreenPlays", IntegerType),
        Property("viralImpressions", IntegerType),
        Property("viralLandingPageClicks", IntegerType),
        Property("viralLikes", IntegerType),
        Property("viralOneClickLeadFormOpens", IntegerType),
        Property("viralOneclickLeads", IntegerType),
        Property("viralOtherEngagements", IntegerType),
        Property("viralReactions", IntegerType),
        Property("viralShares", IntegerType),
        Property("viralTotalEngagements", IntegerType),
        Property("viralVideoCompletions", IntegerType),
        Property("viralVideoFirstQuartileCompletions", IntegerType),
        Property("viralVideoMidpointCompletions", IntegerType),
        Property("viralVideoStarts", IntegerType),
        Property("viralVideoThirdQuartileCompletions", IntegerType),
        Property("viralVideoViews", IntegerType),
    ).to_dict()

    @property
    def adanalyticscolumns(self) -> list[str]:
        """List of columns for adanalytics endpoint."""
        return [
            "clicks,videoMidpointCompletions,videoCompletions,dateRange",
            "costInUsd,landingPageClicks,totalEngagements,videoViews,commentLikes",
            "videoThirdQuartileCompletions,likes,oneClickLeads,fullScreenPlays,videoStarts,videoFirstQuartileCompletions,reactions,costInLocalCurrency",
            "impressions",
        ]

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        return {
            "q": "analytics",
            **super().get_url_params(context, next_page_token),
        }

    def get_unencoded_params(self, context: Context) -> dict:
        """Return a dictionary of unencoded params.

        Args:
            context: The stream context.

        Returns:
            A dictionary of URL query parameters.
        """
        start_date = pendulum.parse(self.config["start_date"])
        end_date = pendulum.parse(self.config["end_date"])
        return {
            "pivot": "CREATIVE",
            "timeGranularity": "DAILY",
            "creatives": f"urn:li:sponsoredCreative:{context['creative_id']}",
            "dateRange.start.year": start_date.year,
            "dateRange.start.month": start_date.month,
            "dateRange.start.day": start_date.day,
            "dateRange.end.year": end_date.year,
            "dateRange.end.month": end_date.month,
            "dateRange.end.day": end_date.day,
            "fields": ",".join(self.adanalyticscolumns),
        }


    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        viral_registrations = row.pop("viralRegistrations", None)
        if viral_registrations:
            row["viralRegistrations"] = int(viral_registrations)

        return super().post_process(row, context)


class _AdAnalyticsByCreativeSecond(_AdAnalyticsByCreativeInit):
    name = "adanalyticsbycreative_second"

    def get_unencoded_params(self, context: Context) -> dict:
        """Return a dictionary of unencoded params.

        Args:
            context: The stream context.

        Returns:
            A dictionary of URL query parameters.
        """
        return {
            **super().get_unencoded_params(context),
            # Overwrite fields with this column subset
            "fields": self.adanalyticscolumns[2],
        }


class _AdAnalyticsByCreativeThird(_AdAnalyticsByCreativeInit):
    name = "adanalyticsbycreative_third"

    def get_unencoded_params(self, context: Context) -> dict:
        """Return a dictionary of unencoded params.

        Args:
            context: The stream context.

        Returns:
            A dictionary of URL query parameters.
        """
        return {
            **super().get_unencoded_params(context),
            # Overwrite fields with this column subset
            "fields": self.adanalyticscolumns[3],
        }


class AdAnalyticsByCreativeStream(_AdAnalyticsByCreativeInit):
    """https://docs.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting#analytics-finder."""

    name = "ad_analytics_by_creative"

    def get_unencoded_params(self, context: Context) -> dict:
        """Return a dictionary of unencoded params.

        Args:
            context: The stream context.

        Returns:
            A dictionary of URL query parameters.
        """
        return {
            **super().get_unencoded_params(context),
            # Overwrite fields with this column subset
            "fields": self.adanalyticscolumns[1],
        }

    def get_records(self, context: dict | None) -> t.Iterable[dict[str, t.Any]]:
        """Return a dictionary of records from adAnalytics classes.

        Combines request columns from multiple calls to the api, which are limited to 20
        columns each.

        Uses `merge_dicts` to combine responses from each class
        super().get_records calls only the records from adAnalyticsByCreative class
        zip() Iterates over the records of adAnalytics classes and merges them with
        merge_dicts() function list() converts each stream context into lists

        Args:
            context: The stream context.

        Returns:
            A dictionary of records given from adAnalytics streams
        """
        adanalyticsinit_stream = _AdAnalyticsByCreativeInit(
            self._tap,
            schema={"properties": {}},
        )
        adanalyticsecond_stream = _AdAnalyticsByCreativeSecond(
            self._tap,
            schema={"properties": {}},
        )
        adanalyticsthird_stream = _AdAnalyticsByCreativeThird(
            self._tap,
            schema={"properties": {}},
        )
        return [
            self.merge_dicts(x, y, z, p)
            for x, y, z, p in zip(
                list(adanalyticsinit_stream.get_records(context)),
                list(super().get_records(context)),
                list(adanalyticsecond_stream.get_records(context)),
                list(adanalyticsthird_stream.get_records(context)),
            )
        ]
