# Review and Rating System

## Overview
This document outlines the review and rating system for the Freelancer-Hirer Marketplace application. The system enables both freelancers and hirers to provide feedback and ratings after contract completion.

## Review Process

### Review Timing
- Reviews can only be submitted after a contract is marked as completed
- Both parties receive a notification to submit a review
- Review period limited to 14 days after contract completion
- Optional reminders sent if review not submitted

### Review Flow
1. Contract is marked as completed
2. Both parties receive review request notification
3. Each party submits their review independently
4. Reviews are revealed to both parties simultaneously after both submit or review period ends
5. One-time option to respond to the received review

## Rating Components

### For Freelancers (rated by Hirers)
- **Overall Rating**: 1-5 stars
- **Specific Criteria**:
  - Quality of work
  - Communication
  - Adherence to deadline
  - Professionalism
  - Technical skills
- **Written Feedback**: Detailed comments about the experience
- **Would hire again**: Yes/No

### For Hirers (rated by Freelancers)
- **Overall Rating**: 1-5 stars
- **Specific Criteria**:
  - Clear communication
  - Payment promptness
  - Reasonable expectations
  - Professionalism
  - Feedback quality
- **Written Feedback**: Detailed comments about the experience
- **Would work again**: Yes/No

## Review Visibility

### Public Display
- Overall rating visible on public profiles
- Summary of ratings for specific criteria
- Number of completed contracts
- Selected review excerpts (with option to hide)

### Private Information
- Full text of all reviews visible only to account owner
- Identity of reviewers for specific reviews
- Detailed breakdown of ratings

## Review Management

### User Controls
- Option to hide a specific review from public profile
- Option to respond to a review once
- Reporting mechanism for inappropriate reviews
- Request for review removal in special circumstances

### Administrative Controls
- Review moderation for inappropriate content
- Review verification to prevent fake reviews
- Manual review intervention in case of disputes
- Automated flagging of suspicious review patterns

## Rating Calculation

### Profile Rating Calculation
- Weighted average of overall ratings
- More recent reviews weighted higher
- Minimum number of reviews required for public display (3)
- Rating trend indicators
- Separate display for different job categories

### Success Metrics
- Completion rate (contracts successfully completed)
- Repeat hire/work rate
- Average project size
- Experience level indicators

## Technical Implementation

### Models
- Review Model
- Rating Model
- ReviewResponse Model
- ReportReview Model

### Views
- Review Submission View
- Review Display View
- Profile Rating Summary View
- Review Management View

### Features
- Review reminder system
- Review analytics and reports
- Filter reviews by date, rating, etc.
- Review export options

## Review Incentives

- Both parties cannot see their received review until they submit their own or the review period ends
- Profile badges for users with high ratings
- Rating history to track improvement over time
- Featured placement for high-rated freelancers
- Special status for consistently well-rated users

## Additional Features

- Rich text formatting for review comments
- Photo/attachment support for reviews
- Featured reviews section on profiles
- Review highlights for quick scanning
- Integration with search ranking algorithm
- Review templates for common feedback 